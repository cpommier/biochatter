import inspect

import pytest

from biochatter._misc import ensure_iterable
from .conftest import calculate_test_score
from .benchmark_utils import (
    skip_if_already_run,
    get_result_file_path,
    write_results_to_file,
)


def test_correctness_of_answers(
    model_name,
    test_data_pdsm,
    conversation,
    multiple_testing,
):
    yaml_data = test_data_pdsm
    task = f"{inspect.currentframe().f_code.co_name.replace('test_', '')}"
    # Wieder einkommentieren, wenn benötigt
    '''skip_if_already_run(
        model_name=model_name, task=task, md5_hash=yaml_data["hash"]
    )'''

    def run_test():
        conversation.reset()  # needs to be reset for each test
        [
            conversation.append_system_message(m)
            for m in yaml_data["input"]["system_messages"]
        ]
        response, _, _ = conversation.query(yaml_data["input"]["prompt"])

        # lower case, remove punctuation
        response = (
            response.lower().replace(".", "").replace("?", "").replace("!", "")
        ).strip()

        print(response)

        score = []

        score.append(response == yaml_data["expected"]["answer"])

        return calculate_test_score(score)

    mean_score, max, n_iterations = multiple_testing(run_test)

    write_results_to_file(
        model_name,
        yaml_data["case"],
        f"{mean_score}/{max}",
        f"{n_iterations}",
        yaml_data["hash"],
        get_result_file_path(task),
    )


