#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0;
uniform vec2 u_texture_count_size_0;

void main() {
    vec3 color = texture(u_texture_0, vec2(uv_0.x * u_texture_count_size_0.x, uv_0.y * u_texture_count_size_0.y)).rgb;
    fragColor = vec4(color, 1.0);
}