from llm.router.model_router import (
    ModelRouter
)


def test_model_router():

    router = ModelRouter()

    response = router.generate(
        prompt="Hello"
    )

    print("\nResponse:")
    print(response)


if __name__ == "__main__":
    test_model_router()