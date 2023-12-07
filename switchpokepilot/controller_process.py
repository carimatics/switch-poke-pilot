import math

import pygame
from reactivex import Subject
from reactivex.operators import debounce
from switch_pilot_core.controller import Button, Hat, ControllerState, StickDisplacementRange, Controller
from switch_pilot_core.libs.serial import SerialPort


def controller_process():
    pygame.init()

    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        return

    state = ControllerState()
    controller = Controller()
    port = SerialPort.get_serial_ports()[0]
    controller.open(port)
    controller.set_state(state)

    axis_dead_zone = 0.15
    axis_center = StickDisplacementRange.CENTER
    axis_input = Subject()
    axis_input.pipe(
        debounce(0.03),
    ).subscribe(
        on_next=lambda _: controller.send(),
        on_error=lambda e: print(e),
        on_completed=lambda: print("completed"),
    )

    buttons = [
        Button.A,
        Button.B,
        Button.X,
        Button.Y,
        Button.MINUS,
        Button.HOME,
        Button.PLUS,
        Button.L_CLICK,
        Button.R_CLICK,
        Button.L,
        Button.R,
        Hat.TOP,
        Hat.BOTTOM,
        Hat.LEFT,
        Hat.RIGHT,
        Button.CAPTURE,
    ]

    def process_axis(value: float, handler):
        level = axis_center if abs(value) <= axis_dead_zone else math.ceil(value * 127.5 + 127.5)
        handler(level)

    def handle_l_stick_x(level: int):
        state.l_stick.x = level
        axis_input.on_next(None)

    def handle_l_stick_y(level: int):
        state.l_stick.y = level
        axis_input.on_next(None)

    def handle_r_stick_x(level: int):
        state.r_stick.x = level
        axis_input.on_next(None)

    def handle_r_stick_y(level: int):
        state.r_stick.y = level
        axis_input.on_next(None)

    def handle_z(button: Button, level: int):
        if level > 0:
            state.set(buttons=[button])
        else:
            state.unset(buttons=[button])
        controller.send()

    axis_handlers = [
        lambda level: handle_l_stick_x(level),
        lambda level: handle_l_stick_y(level),
        lambda level: handle_r_stick_x(level),
        lambda level: handle_r_stick_y(level),
        lambda level: handle_z(Button.ZL, level),
        lambda level: handle_z(Button.ZR, level),
    ]

    clock = pygame.time.Clock()

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.JOYAXISMOTION:
                    process_axis(event.value, axis_handlers[event.axis])

                elif event.type == pygame.JOYBUTTONDOWN:
                    if 11 <= event.button <= 14:
                        state.set(hat=buttons[event.button])
                    else:
                        state.set(buttons=[buttons[event.button]])
                    controller.send()

                elif event.type == pygame.JOYBUTTONUP:
                    if 11 <= event.button <= 14:
                        state.unset(hat=True)
                    else:
                        state.unset(buttons=[buttons[event.button]])
                    controller.send()
            clock.tick(45)

    except KeyboardInterrupt:
        pass

    finally:
        pygame.quit()
