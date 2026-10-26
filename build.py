
import argparse
import random
from pathlib import Path

SEED = 42

TASKS = [
    "roles",
]

DEFAULT_COUNTS = {
    'train': 1000,
    'valid': 200,
    'test': 200
    }

INTRO_FRAMES = [
    'I want to {activity}.', "I'd like to {activity}.",
    'I would like to {activity}.', 'I plan to {activity}.',
    "I'm planning to {activity}.", 'I intend to {activity}.',
    "I'm hoping to {activity}.", 'My plan is to {activity}.',
    "I've decided to {activity}.", 'I would really like to {activity}.',
    'I feel ready to {activity}.', 'I would prefer to {activity}.',
]
INTRO_TIMES = ['', ' today', ' tomorrow', ' this weekend', ' soon', ' when I have time']


def intro_text(rng, action, value=None):
    from actions import ACTIVITY_PHRASES
    unknown, known = ACTIVITY_PHRASES[action[0]]
    activity = unknown if value is None else known.format(value=value)
    return rng.choice(INTRO_FRAMES).format(activity=activity + rng.choice(INTRO_TIMES))


def make_dialogue(rng, task, action):
    verb, thing, ask, values = action
    value = rng.choice(values)
    initial_known = task in ('roles', 'questions') and rng.choice([True, False])
    intro = intro_text(rng, action, value if initial_known else None)
    # Each User turn stores information explicitly supplied by that turn.
    turns = [('User', intro, value if initial_known else None)]
    if task in ('roles', 'questions'):
        return turns


def render(rng, task, action):
    verb, _, ask, _ = action
    turns = make_dialogue(rng, task, action)


def build(out, counts):
    from actions import ACTIONS

    # Reserve evaluation inputs first: changing only --train keeps valid/test fixed.
    for split in ('valid', 'test', 'train'):
        if split not in counts:
            continue
        rng = random.Random(SEED)
        
        for i in range(counts[split]):
            task = TASKS[i % len(TASKS)]
            
            for action in ACTIONS:

                story = render(rng, task, action)



if __name__ == '__main__':

    products_dir = Path(__file__).resolve().parent / 'products'

    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=products_dir)
    parser.add_argument('--train', type=int, default=DEFAULT_COUNTS['train'])
    parser.add_argument('--valid', type=int, default=DEFAULT_COUNTS['valid'])
    parser.add_argument('--test', type=int, default=DEFAULT_COUNTS['test'])

    args = parser.parse_args()
    try:
        build(args.out, {
            'train': args.train,
            'valid': args.valid,
            'test': args.test
            })
    except ValueError as error:
        parser.error(str(error))
