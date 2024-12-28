class BedslingerAlignHelper:
    def __init__(self, config):
        self.config = config
        self.printer = config.get_printer()
        self.printer.register_event_handler("klippy:ready", self.handle_ready)

        self.safe_x_pos = config.getfloat('safe_x_pos')
        self.initial_z_height = config.getfloat('initial_z_height')
        self.initial_move_speed = config.getfloat('initial_move_speed')
        self.align_step_size_initial = config.getfloat('align_step_size_initial')
        self.align_step_size_precise = config.getfloat('align_step_size_precise')
        self.align_step_speed = config.getfloat('align_step_speed')
        self.align_step_accel = config.getfloat('align_step_accel')
        self.align_backtrack = config.getfloat('align_backtrack')
        self.backtrack_distance = config.getfloat('backtrack_distance')

        endstop_pins = config.getlist('z_endstops')
        ppins = self.printer.lookup_object('pins')

        self.endstops = []
        for endstop_pin in endstop_pins:
            self.endstops.append(ppins.setup_pin('endstop', endstop_pin))

        self.force_move = None

    def handle_ready(self):
        self.toolhead = self.printer.lookup_object('toolhead')
        self.force_move = self.printer.load_object(self.config, 'force_move')

    def _query_endstop_state(self):
        res = []
        print_time = self.toolhead.get_last_move_time()
        for endstop in self.endstops:
            res.append(endstop.query_endstop(print_time))
        return res

    def _all_endstops_triggered(self):
        return all(self._query_endstop_state())

    def _alignment_step(self, is_precise = False):
        endstop_state = self._query_endstop_state()

        step = self.align_step_size_initial
        if is_precise:
            step = self.align_step_size_precise

        for i in range(len(self.endstops)):
            stepper_name = 'stepper_z'
            if i != 0:
                stepper_name += str(i)

            if not endstop_state[i]:
                self.force_move.manual_move(self.force_move.lookup_stepper(stepper_name), step,
                                            self.align_step_speed, self.align_step_accel)

    def do_z_align(self):
        gcode = self.printer.lookup_object('gcode')

        gcode.respond_info('Gantry alignment started. Gantry moving to initial position: Z' + str(self.initial_z_height))
        initial_pos = self.toolhead.get_position()
        initial_pos[0] = self.safe_x_pos
        initial_pos[2] = self.initial_z_height
        self.toolhead.move(initial_pos, self.initial_move_speed)

        # Initial search
        while not self._all_endstops_triggered():
            self._alignment_step()

        # Backtrack
        initial_pos[2] = initial_pos[2] - self.align_backtrack
        self.toolhead.move(initial_pos, self.initial_move_speed)

        # Precise search
        while not self._all_endstops_triggered():
            self._alignment_step(is_precise=True)

        initial_pos[2] = initial_pos[2] - self.backtrack_distance
        self.toolhead.move(initial_pos, self.initial_move_speed)
        gcode.respond_info('Alignment finished, Z homing required!')

class ZGantryAlign:
    cmd_BEDSLINGER_GANTRY_ALIGN_help = 'Auto Z gantry alignment'

    def __init__(self, config):
        self.printer = config.get_printer()
        self.helper = BedslingerAlignHelper(config)
        gcode = self.printer.lookup_object('gcode')
        gcode.register_command('BEDSLINGER_GANTRY_ALIGN', self.cmd_BEDSLINGER_GANTRY_ALIGN, self.cmd_BEDSLINGER_GANTRY_ALIGN_help)

    def cmd_BEDSLINGER_GANTRY_ALIGN(self, gcmd):
        self.helper.do_z_align()

def load_config(config):
    return ZGantryAlign(config)
