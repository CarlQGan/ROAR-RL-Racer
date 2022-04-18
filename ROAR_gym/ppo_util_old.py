from pathlib import Path
from typing import Optional, Dict

import gym
import torch as th
from torch import nn

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class CustomMaxPoolCNN(BaseFeaturesExtractor):
    """
    the CNN network that interleaves convolution & maxpooling layers, used in a
    previous DQN implementation and shows reasonable results
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        super(CustomMaxPoolCNN, self).__init__(observation_space, features_dim)
        # We assume CxWxH images (channels last)
        n_input_channels = observation_space.shape[0]

        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 6, kernel_size=(5, 5)),
            nn.ReLU(),
            nn.Conv2d(6, 12, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.Conv2d(12, 24, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            nn.Conv2d(24, 48, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.Conv2d(48, 96, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            nn.Conv2d(96, 96, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.Conv2d(96, 96, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2)),
            nn.Conv2d(96, 96, kernel_size=(3, 3)),
            nn.ReLU(),
            nn.Conv2d(96, 96, kernel_size=(4, 4)),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.cnn(
                th.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, n_flatten*2), nn.ReLU(),
                                    nn.Linear(n_flatten*2, n_flatten), nn.ReLU(),
                                    nn.Linear(n_flatten, features_dim),)

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))


class CustomMaxPoolCNN_no_map(BaseFeaturesExtractor):
    """
    the CNN network that interleaves convolution & maxpooling layers, used in a
    previous DQN implementation and shows reasonable results
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        super(CustomMaxPoolCNN_no_map, self).__init__(observation_space, features_dim)
        # We assume CxWxH images (channels last)
        n_input_channels = observation_space.shape[0]

        self.linear = nn.Sequential(nn.Linear(n_input_channels, 64), nn.ReLU(),
                                    nn.Linear(64, 128), nn.ReLU(),
                                    nn.Linear(128, 256), nn.ReLU(),
                                    nn.Linear(256, 256), nn.ReLU(),
                                    nn.Linear(256, 256), nn.ReLU(),
                                    nn.Linear(256, features_dim),)

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(observations)

def find_latest_model(root_path: Path) -> Optional[Path]:
    import os
    from pathlib import Path
    logs_path = (root_path / "logs")
    if logs_path.exists() is False:
        print(f"No previous record found in {logs_path}")
        return None
    paths = sorted(logs_path.iterdir(), key=os.path.getmtime)
    paths_dict: Dict[int, Path] = {
        int(path.name.split("_")[2]): path for path in paths
    }
    if len(paths_dict) == 0:
        return None
    latest_model_file_path: Optional[Path] = paths_dict[max(paths_dict.keys())]
    return latest_model_file_path
