cmake_minimum_required(VERSION 3.10)
project(DockerLintProject LANGUAGES NONE)

# --- Parse .env file ---
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.env")
    file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/.env" ENV_LINES)
    foreach(LINE ${ENV_LINES})
        if(LINE MATCHES "^([^=]+)=(.*)$")
            set(VAR_NAME ${CMAKE_MATCH_1})
            set(VAR_VALUE ${CMAKE_MATCH_2})
            set(VAR_VALUE_CLEAN ${CMAKE_MATCH_2})
            string(STRIP ${VAR_VALUE_CLEAN} VAR_VALUE_CLEAN)
            set(ENV_${VAR_NAME} ${VAR_VALUE_CLEAN})
        endif()
    endforeach()
endif()

# Fallback values
if(NOT ENV_DOCKER_NAME)
    set(ENV_DOCKER_NAME "task")
endif()
if(NOT ENV_DOCKER_TAG)
    set(ENV_DOCKER_TAG "test")
endif()

set(DOCKER_IMAGE_NAME "${ENV_DOCKER_NAME}")
set(DOCKER_IMAGE_TAG "${ENV_DOCKER_TAG}")
set(DOCKER_FULL_NAME "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")

# 1. Build Base Image
add_custom_target(
    docker-build-base
    COMMAND docker build --target base -t "${DOCKER_IMAGE_NAME}:base" .
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Building base Docker image..."
    VERBATIM
)

# 2. Lint (sync changes with volume)
# We split the commands for better reliability and use VERBATIM to handle quotes correctly
add_custom_target(
    docker-lint
    COMMAND docker run --rm -v "${CMAKE_CURRENT_SOURCE_DIR}:/app" "${DOCKER_IMAGE_NAME}:base" python -m isort src test
    COMMAND docker run --rm -v "${CMAKE_CURRENT_SOURCE_DIR}:/app" "${DOCKER_IMAGE_NAME}:base" python -m black src test
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS docker-build-base
    COMMENT "Linting and formatting code (syncing changes)..."
    VERBATIM
)

# 3. Static Analysis & Tests
add_custom_target(
    docker-test
    COMMAND docker build --target tester -t "${DOCKER_IMAGE_NAME}:tester" .
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS docker-lint
    COMMENT "Running static analysis (flake8) and unit tests..."
    VERBATIM
)

# 4. Final Build
add_custom_target(
    docker-build
    COMMAND docker build -t "${DOCKER_FULL_NAME}" .
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS docker-test
    COMMENT "Building final production image: ${DOCKER_FULL_NAME}"
    VERBATIM
)
