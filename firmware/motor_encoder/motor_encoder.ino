	const int LEFT_ENCODER_A = -1;
const int RIGHT_ENCODER_A = -1;
float left_motor_command = 0.0;
float right_motor_command = 0.0;
volatile long left_encoder_ticks = 0;
volatile long right_encoder_ticks = 0;
long previous_left_ticks = 0;
long previous_right_ticks = 0;

float left_wheel_speed = 0.0;
float right_wheel_speed = 0.0;

// Hardware-dependent parameters
const float WHEEL_RADIUS = 0.0;   // meters, set when hardware is known
const int ENCODER_CPR = 0;        // counts per revolution
// Encoder interrupt handlers

void leftEncoderISR()
{
  left_encoder_ticks++;
}

void rightEncoderISR()
{
  right_encoder_ticks++;
}

unsigned long last_publish_time = 0;
const unsigned long publish_interval = 100;  // 10 Hz

void setMotorCommands(float left, float right)
{
  // TODO:
  // Convert motor commands to PWM and direction signals
  // Implementation depends on the real motor driver
}

void updateWheelSpeeds(unsigned long elapsed_ms)
{
  long current_left_ticks;
  long current_right_ticks;

  // Safely copy encoder values modified by interrupts
  noInterrupts();
  current_left_ticks = left_encoder_ticks;
  current_right_ticks = right_encoder_ticks;
  interrupts();

  long delta_left = current_left_ticks - previous_left_ticks;
  long delta_right = current_right_ticks - previous_right_ticks;

  if (ENCODER_CPR > 0 && WHEEL_RADIUS > 0.0 && elapsed_ms > 0)
  {
    float dt = elapsed_ms / 1000.0;
    float meters_per_tick =
      (2.0 * PI * WHEEL_RADIUS) / ENCODER_CPR;

    left_wheel_speed =
      delta_left * meters_per_tick / dt;

    right_wheel_speed =
      delta_right * meters_per_tick / dt;
  }

  previous_left_ticks = current_left_ticks;
  previous_right_ticks = current_right_ticks;
}

void setup()
{
  Serial.begin(115200);
  if (LEFT_ENCODER_A >= 0)
  {
    pinMode(LEFT_ENCODER_A, INPUT_PULLUP);
    attachInterrupt(
      digitalPinToInterrupt(LEFT_ENCODER_A),
      leftEncoderISR,
      RISING
    );
  }

  if (RIGHT_ENCODER_A >= 0)
  {
    pinMode(RIGHT_ENCODER_A, INPUT_PULLUP);
    attachInterrupt(
      digitalPinToInterrupt(RIGHT_ENCODER_A),
      rightEncoderISR,
      RISING
    );
  }
  // TODO:
  // Configure motor driver pins
  // Configure encoder pins
  // Attach encoder interrupts
}

void loop()
{
  // TODO:
  // Read motor commands
  // Control left and right motors
  if (Serial.available() > 0)
  {
    left_motor_command = Serial.parseFloat();
    right_motor_command = Serial.parseFloat();
    setMotorCommands(left_motor_command, right_motor_command);
  }
  // Calculate wheel speed

  // Publish encoder counts at 10 Hz
  unsigned long current_time = millis();

  if (current_time - last_publish_time >= publish_interval)
  {
    unsigned long elapsed_ms = current_time - last_publish_time;
    last_publish_time = current_time;

    updateWheelSpeeds(elapsed_ms);

    Serial.print(left_encoder_ticks);
    Serial.print(",");
    Serial.print(right_encoder_ticks);
    Serial.print(",");
    Serial.print(left_wheel_speed);
    Serial.print(",");
    Serial.println(right_wheel_speed);
  }
}
