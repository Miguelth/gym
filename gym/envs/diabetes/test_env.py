import numpy as np
import gym
# import seaborn as sns
# sns.set()

from pylab import plot, figure, title, show, ion

env = gym.make('HovorkaGaussian-v0')
# env = gym.make('HovorkaGaussianInsulin-v0')
# env = gym.make('HovorkaBinary-v0')
# env = gym.make('HovorkaAbsolute-v0')


# basal = 0
# env.env.init_bg = 110

env.reset()
reward = []

for i in range(336):

    # Step for the minimal/hovorka model
    s, r, d, i = env.step(np.array([6.6]))
    reward.append(r)
    # print(r)

    # Step for the discrete Hovorka incremental
    # env.step(2)



# env.render()
figure()
plot(env.env.bg_history)
title('bg')
ion()
show()

figure()
plot(reward)
title('reward')
show()

