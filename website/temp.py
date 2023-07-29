from threading import Lock


class Temp():
    def __init__(self, temp=0, power=0) -> None:
        self._lock_temp = Lock()
        self._lock_power = Lock()
        self._temp = temp
        self._power = power
        self._pid_prev_error = 0
        self._is_start_plant = False

    def start_plant(self):
        self._is_start_plant = True

    def stop_plant(self):
        self._is_start_plant = False

    def get_temp(self):
        with self._lock_temp:
            return self._temp

    # pu_temp methods will automatically updates the temperature and power value.
    def put_temp(self, temp):
        with self._lock_temp, self._lock_power:
            self._temp = temp
            self._power, self._pid_prev_error = self.calc_power(self._pid_prev_error)
            self._power = min(self._power, 100)
            self._power = max(self._power, 10)

    def get_power(self):
        with self._lock_power:
            if self._is_start_plant:
                return self._power
            return 0

    def calc_power(self,
                   pid_prev_error,
                   # PI-PD parameters
                   Kp = 15.2,                    # Proportional gain
                   Ki = 3.5,                    # Integral gain
                   Kd = 0.05,                    # Derivative gain
                   setpoint         = 40.0,     # Setpoint temperature (desired temperature)
                   integral_limit   = 100.0     # Integral term upper limit
    ):
        error = setpoint - self._temp
        # Calculate the proportional, derivative and integral terms.
        # The integral terms is cap to avoid instability.
        proportional = Kp * error
        integral = Ki * error
        integral = max(-integral_limit, min(integral, integral_limit))
        derivative = Kd * (error - pid_prev_error)
        pid_prev_error = error

        # Calculate PI-PD output
        output = proportional + integral + derivative
        return output, pid_prev_error
