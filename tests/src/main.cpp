#include <iostream>
#include <glm/glm.hpp>
#include <nlohmann/json.hpp>
#include <fmt/base.h>
#include <spdlog/spdlog.h>

using json = nlohmann::json;

json vec3_to_json(const glm::vec3& v) {
    return json{
        {"x", v.x},
        {"y", v.y},
        {"z", v.z}
    };
}

glm::vec3 json_to_vec3(const json& j) {
    return glm::vec3(
        j.at("x").get<float>(),
        j.at("y").get<float>(),
        j.at("z").get<float>()
    );
}

int main() {
    fmt::print("Hello from fmt\n");
    spdlog::info("Welcome to spdlog!");

    glm::vec3 position(1.5f, -2.0f, 3.25f);

    json j = vec3_to_json(position);
    std::cout << "Serialized vec3 to JSON" << j.dump(4) << std::endl;

    glm::vec3 deserialized = json_to_vec3(j);
    std::cout << "Deserialized JSON to vec3: ("
        << deserialized.x << ", "
        << deserialized.y << ", "
        << deserialized.z << ")" << std::endl;

    return 0;
}