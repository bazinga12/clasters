import itertools
import pytest
import main

def test_immutability():
    data = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
    }

    actual = {
        'ginger': {
            'django': 2,
            'flask': 3,
            'pylons': 1,
        },
        'cucumber': {
            'flask': 1,
            'pylons': 6,
        },
    }

    update = main.preserve_immutability(main.update)
    expected = update(data, 'pylons', 7)
    assert expected == actual
    assert expected is not actual
    assert all(expected[claster] is not actual[claster] for claster in expected)


def test_update():
    config = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
    }

    main.update(config, 'pylons', 7)
    assert config == {
        'ginger': {
            'django': 2,
            'flask': 3,
            'pylons': 1,
        },
        'cucumber': {
            'flask': 1,
            'pylons': 6,
        },
    }


def test_initial():
    config = {
        'ginger': {},
        'cucumber': {},
    }

    main.update(config, 'flask', 3)
    main.update(config, 'django', 3)

    assert sum(config['ginger'].values()) == sum(config['cucumber'].values())
    assert sum(sum(x.values()) for x in config.values()) == 3+3


@pytest.mark.xfail(reason="Advanced test. Optional to implement")
def test_predictable_config():
    permutations = []
    services = [
        ('flask', 7),
        ('django', 13),
        ('pylons', 17)
    ]

    for permutation in itertools.permutations(services):
        config = {
            'ginger': {},
            'cucumber': {},
        }
        for svc, num in permutation:
            main.update(config, svc, num)
        assert sum(sum(x.values()) for x in config.values()) == 7+13+17
        permutations.append(config)

    assert all(p == permutations[0] for p in permutations[1:])
