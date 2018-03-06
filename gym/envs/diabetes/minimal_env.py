"""
OPENAI gym environment for the minimal model
"""

import logging
import gym
from gym import spaces

import numpy as np
import numpy.matlib
from scipy.integrate import ode

# Plotting for the rendering
import matplotlib.pyplot as plt

# Hovorka simulator
from gym.envs.diabetes import minimal_model as mm
from gym.envs.diabetes.hovorka_model import hovorka_parameters


logger = logging.getLogger(__name__)

class MinimalDiabetes(gym.Env):
    # TODO: fix metadata
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        """
        Initializing the simulation environment.
        """

        # Continuous action space -- pump rate
        # The maximum rate on the Medtronic minimed pumps is
        # 583 mU/min. We round down to a max rate of 500
        self.action_space = spaces.Box(0, 500, 1)

        # Continuous observation space
        self.observation_space = spaces.Box(0, 500, 2)

        self._seed()
        self.viewer = None

        # =====================
        # Ode solvers
        # =====================

        # Models
        self.integrator_carb = ode(mm.carb_model)
        self.integrator_insulin = ode(mm.insulin_model)

        # Solver setup
        self.integrator_carb.set_integrator('dop853')
        self.integrator_insulin.set_integrator('dop853')

        # Initial values
        self.init_deviation = np.random.choice(range(70, 150, 1), 1)
        # self.init_deviation = 300
        self.integrator_carb.set_initial_value(np.array([0, 0, 0]))
        self.integrator_insulin.set_initial_value(np.array([self.init_deviation, 0]))

        # Hovorka parameters
        self.P = hovorka_parameters(70)

        # Counter for number of iterations
        self.num_iters = 0

        # If blood glucose is less than zero, the simulator is out of bounds.
        self.bg_threshold_low = 0
        self.bg_threshold_high = 500

        self.bg_history = []
        self.insulin_history = []

        self.max_iter = 3000

        self.steps_beyond_done = None


    def _step(self, action):
        """
        Set the insulin pump rate
        """
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        # Running the simulation for one step

        # The action is the insulin pump ratio
        self.integrator_carb.set_f_params(0, self.P)
        self.integrator_carb.integrate(self.integrator_carb.t + 1)

        self.integrator_insulin.set_f_params(action, self.integrator_carb.y[2], self.P)
        self.integrator_insulin.integrate(self.integrator_insulin.t + 1)

        # Updating state
        # bg = self.integrator_insulin.y[0] + 90
        bg = self.integrator_insulin.y[0]
        insulin = self.integrator_insulin.y[1]
        self.state = [bg, insulin]

        self.num_iters += 1

        # Updating environment parameters
        self.bg_history.append(bg)
        self.insulin_history.append(insulin)


        #Set environment done = True if blood_glucose_level is negative
        done = 0

        if (bg > self.bg_threshold_high or bg < self.bg_threshold_low):
            done = 1

        if self.num_iters > self.max_iter:
            done = 1

        done = bool(done)

        # ====================================================================================
        # Calculate Reward  (and give error if action is taken after terminal state)
        # ====================================================================================

        if not done:

            # reward_flag = 9
            reward_flag = 3

            if reward_flag == 1:
                ''' Binary reward function'''
                low_bg = 70
                high_bg = 120

                if np.max(blood_glucose_level) < high_bg and np.min(blood_glucose_level) > low_bg:
                    reward = 1
                else:
                    reward = 0

            elif reward_flag == 2:
                ''' Squared cost function '''
                bg_ref = 90

                reward = - (blood_glucose_level - bg_ref)**2

            elif reward_flag == 3:
                ''' Absolute cost function '''
                bg_ref = 90

                reward = - abs(blood_glucose_level - bg_ref)

            # elif reward_flag == 4:
                # ''' Squared cost with insulin constraint '''
                # bg_ref = 80

                # reward = - (blood_glucose_level - bg_ref)**2
            else:
                ''' Gaussian reward function '''
                bg_ref = 90
                h = 30

                # reward =  10 * np.exp(-0.5 * (blood_glucose_level - bg_ref)**2 /h**2) - 5
                reward =  np.exp(-0.5 * (blood_glucose_level - bg_ref)**2 /h**2)

        elif self.steps_beyond_done is None:
            # Blood glucose below zero -- simulation out of bounds
            self.steps_beyond_done = 0
            reward = -1000
        else:
            if self.steps_beyond_done == 0:
                logger.warning("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = -1000

        return np.array(self.state), reward, done, {}

    def _reset(self):
        #TODO: Insert init code here!

        # self.init_deviation = np.random.choice(range(20, 30, 20), 1)
        self.init_deviation = np.random.choice(range(70, 150, 1), 1)
        # self.init_deviation = 300

        # Initial values
        self.integrator_carb.set_initial_value(np.array([0, 0, 0]))

        self.integrator_insulin.set_initial_value(np.array([self.init_deviation, 0]))

        # self.state = [90]
        # self.state = [self.init_deviation + 90, 0]
        self.state = [self.init_deviation, 0]

        self.bg_history = []
        self.insulin_history = []

        self.num_iters = 0

        self.steps_beyond_done = None

        return np.array(self.state)


    def _render(self, mode='human', close=False):
        #TODO: Clean up plotting routine

        if mode == 'rgb_array':
            return None
        elif mode is 'human':
            # if not bool(plt.get_fignums()):
            if not 999 in plt.get_fignums():
                plt.ion()
                self.fig = plt.figure(999)
                self.ax = self.fig.add_subplot(111)
                # self.line1, = ax.plot(self.bg_history)
                self.ax.plot(self.bg_history)
                plt.show()
            else:
                # self.line1.set_ydata(self.bg_history)
                # self.fig.canvas.draw()
                self.ax.clear()
                self.ax.plot(self.bg_history)

            plt.pause(0.0000001)
            plt.show()

            return None
        else:
            super(MinimalDiabetes, self).render(mode=mode) # just raise an exception

            plt.ion()
            plt.plot(self.bg_history)

    def _close(self):
        ''' closing the rendering'''
        plt.close(1000)
