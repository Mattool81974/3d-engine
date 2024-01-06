#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;
layout (location = 3) in float in_face;

out float face_0;
out vec2 uv_0;

uniform mat4 m_model;
uniform mat4 m_proj;
uniform mat4 m_view;

void main() {
    in_normal;

    face_0 = in_face;
    uv_0 = in_texcoord_0;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}