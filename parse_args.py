import argparse

from config_hndlr import parse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_dir", type=str, default="configs/runs")
    parser.add_argument("--env_id", type=str, default="bullet")
    parser.add_argument("--agent_id", type=str, default="ktd")
    parser.add_argument("--seed", type=int, default=2)

    config = parse(parser)
    return config


