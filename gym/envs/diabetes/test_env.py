import numpy as np
import gym
import seaborn as sns
sns.set()

from pylab import plot, figure, title, show, ion

# env = gym.make('HovorkaDiabetes-v0')
# env = gym.make('HovorkaInterval-v0')
# env = gym.make('HovorkaIntervalRandom-v0')
# env = gym.make('MinimalDiabetes-v0')
# env = gym.make('MinimalDiabetesYasini-v0')
# env = gym.make('YasiniMeals-v0')
# env = gym.make('HovorkaMeals-v0')
# env = gym.make('HovorkaHovorka-v0')
# env = gym.make('HovorkaRandomGaussianInsulin-v0')
# env = gym.make('HovorkaGaussianInsulin-v0')
env = gym.make('HovorkaIntervalMeals-v0')



# basal = 0
# env.env.init_bg = 110

env.reset()
reward = []

for i in range(96):

    # Step for the minimal/hovorka model
    s, r, d, i = env.step(np.array([6.6]))
    # reward.append(r)
    # print(r)

    # Step for the discrete Hovorka incremental
    # env.step(2)



# env.render()
figure()
plot(env.env.bg_history)
ion()
show()

# figure()
# plot(reward)
# show()

