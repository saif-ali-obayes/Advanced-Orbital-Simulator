import matplotlib.pyplot as plt
import numpy as np

# الثوابت الفيزيائية الأساسية
G = 6.67430e-11
M_earth = 5.97219e24
mu = G * M_earth

R_e = 6378137.0  # نصف قطر الأرض الاستوائي بالمتر
J2 = 1.08263e-3  # معامل تفلطح الأرض

# الشروط الابتدائية في الفضاء الثلاثي (3D) مع إحداثيات الميلان المداري
r_perigee = R_e + 400e3  # الحضيض (400 كم)
r_apogee = R_e + 1000e3  # الأوج (1000 كم)
r0 = np.array([r_perigee, 0.0, 0.0], dtype=float)

# حساب السرعة الابتدائية وتطبيق زاوية ميلان مداري (Inclination = 28.5 درجة مثلاً)
v_mag_perigee = np.sqrt(
    mu * ((2.0 / r_perigee) - (1.0 / ((r_perigee + r_apogee) / 2.0)))
)
inclination = np.radians(28.5)  # زاوية الميلان المداري
v0 = np.array(
    [
        0.0,
        v_mag_perigee * np.cos(inclination),
        v_mag_perigee * np.sin(inclination),
    ],
    dtype=float,
)

# زمن المحاكاة والخطوات الزمنية
dt = 5.0
total_time = 300 * 60  # 5 ساعات محاكاة
steps = int(total_time / dt)

# معاملات السحب الجوي
Cd = 2.2
A = 2.2
m = 150.0
rho0 = 1.225
H = 8500.0

# معاملات الدفع الصاروخي (Orbital Maneuver)
thrust_start_time = 40 * 60
thrust_duration = 5 * 60
thrust_acc = 0.05


# دالة حساب التسارع الشاملة في الفضاء ثلاثي الأبعاد (3D)
def get_acceleration(r_vec, v_vec, current_time):
  r_mag = np.linalg.norm(r_vec)
  x, y, z = r_vec[0], r_vec[1], r_vec[2]
  current_altitude = r_mag - R_e

  # 1. الجاذبية الأساسية
  a_grav = -mu * r_vec / (r_mag**3)

  # 2. تفلطح الأرض (J2 Perturbation) في 3D بدقة تامة
  z2_r2 = (z / r_mag) ** 2
  factor = (1.5 * J2 * mu * (R_e**2)) / (r_mag**5)
  a_j2 = factor * np.array(
      [x * (5.0 * z2_r2 - 1.0), y * (5.0 * z2_r2 - 1.0), z * (5.0 * z2_r2 - 3.0)]
  )

  # 3. المقاومة الجوية
  a_drag = np.array([0.0, 0.0, 0.0], dtype=float)
  if 0 < current_altitude < 800e3:
    v_mag = np.linalg.norm(v_vec)
    rho = (
        rho0 * np.exp(-current_altitude / H) if current_altitude > 0 else rho0
    )
    drag_magnitude = 0.5 * rho * (v_mag**2) * Cd * A / m
    if v_mag > 0:
      a_drag = -drag_magnitude * (v_vec / v_mag)

  # 4. الدفع الصاروخي (Prograde Thrust)
  a_thrust = np.array([0.0, 0.0, 0.0], dtype=float)
  if (
      thrust_start_time
      <= current_time
      <= (thrust_start_time + thrust_duration)
  ):
    v_mag = np.linalg.norm(v_vec)
    if v_mag > 0:
      a_thrust = thrust_acc * (v_vec / v_mag)

  return a_grav + a_j2 + a_drag + a_thrust


# مصفوفات التخزين الثلاثية
positions = np.zeros((steps, 3))
positions[0] = r0

r = np.copy(r0)
v = np.copy(v0)
current_time = 0.0

# حلقة المحاكاة باستخدام RK4
for i in range(1, steps):
  dr1 = v
  dv1 = get_acceleration(r, v, current_time)

  r2 = r + 0.5 * dt * dr1
  v2 = v + 0.5 * dt * dv1
  dr2 = v2
  dv2 = get_acceleration(r2, v2, current_time + 0.5 * dt)

  r3 = r + 0.5 * dt * dr2
  v3 = v + 0.5 * dt * dv2
  dr3 = v3
  dv3 = get_acceleration(r3, v3, current_time + 0.5 * dt)

  r4 = r + dt * dr3
  v4 = v + dt * dv3
  dr4 = v4
  dv4 = get_acceleration(r4, v4, current_time + dt)

  r = r + (dt / 6.0) * (dr1 + 2 * dr2 + 2 * dr3 + dr4)
  v = v + (dt / 6.0) * (dv1 + 2 * dv2 + 2 * dv3 + dv4)

  positions[i] = r
  current_time += dt

# إعداد نافذة الرسم ثلاثي الأبعاد (3D Plotting)
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')

# رسم مجسم الأرض الكروي ثلاثي الأبعاد
u = np.linspace(0, 2 * np.pi, 40)
v_angles = np.linspace(0, np.pi, 40)
x_earth = R_e * np.outer(np.cos(u), np.sin(v_angles))
y_earth = R_e * np.outer(np.sin(u), np.sin(v_angles))
z_earth = R_e * np.outer(np.ones(np.size(u)), np.cos(v_angles))

ax.plot_surface(
    x_earth,
    y_earth,
    z_earth,
    color='dodgerblue',
    alpha=0.3,
    linewidth=0,
    antialiased=True,
)

# رسم مسار المدار ثلاثي الأبعاد والمائل
ax.plot(
    positions[:, 0],
    positions[:, 1],
    positions[:, 2],
    color='purple',
    linewidth=1.5,
    label='3D Inclined Orbit (RK4 + J2 + Drag + Thrust)',
)

ax.set_title(
    'Advanced 3D Astrodynamics Simulation', fontsize=11, fontweight='bold'
)
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')
ax.legend(loc='upper left')
# حفظ الصورة الثلاثية الأبعاد للملفات النهائية
plt.savefig('3d_orbital_simulation.png', dpi=300, bbox_inches='tight')
plt.show()