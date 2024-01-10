#version 330 core

layout (location = 0) out vec4 fragColor;

in float face_0;
in vec2 uv_0;

uniform sampler2D u_texture_0;
uniform sampler2D u_texture_1;
uniform sampler2D u_texture_2;
uniform sampler2D u_texture_3;
uniform sampler2D u_texture_4;
uniform sampler2D u_texture_5;
uniform sampler2D u_texture_6;
uniform sampler2D u_texture_7;
uniform vec2 u_texture_count_size_0;
uniform vec2 u_texture_count_size_1;
uniform vec2 u_texture_count_size_2;
uniform vec2 u_texture_count_size_3;
uniform vec2 u_texture_count_size_4;
uniform vec2 u_texture_count_size_5;
uniform vec2 u_texture_count_size_6;
uniform vec2 u_texture_count_size_7;

void main() {
    vec4 color = vec4(face_0/5.0, 0.0, 0.0, 1.0);

    if(face_0 == 0.0) {color = texture(u_texture_0, vec2(uv_0.x * u_texture_count_size_0.x, uv_0.y * u_texture_count_size_0.y));}
    else if(face_0 == 1.0) {color = texture(u_texture_1, vec2(uv_0.x * u_texture_count_size_1.x, uv_0.y * u_texture_count_size_1.y));}
    else if(face_0 == 2.0) {color = texture(u_texture_2, vec2(uv_0.x * u_texture_count_size_2.x, uv_0.y * u_texture_count_size_2.y));}
    else if(face_0 == 3.0) {color = texture(u_texture_3, vec2(uv_0.x * u_texture_count_size_3.x, uv_0.y * u_texture_count_size_3.y));}
    else if(face_0 == 4.0) {color = texture(u_texture_4, vec2(uv_0.x * u_texture_count_size_4.x, uv_0.y * u_texture_count_size_4.y));}
    else if(face_0 == 5.0) {color = texture(u_texture_5, vec2(uv_0.x * u_texture_count_size_5.x, uv_0.y * u_texture_count_size_5.y));}
    else if(face_0 == 6.0) {color = texture(u_texture_6, vec2(uv_0.x * u_texture_count_size_6.x, uv_0.y * u_texture_count_size_6.y));}
    else if(face_0 == 7.0) {color = texture(u_texture_7, vec2(uv_0.x * u_texture_count_size_7.x, uv_0.y * u_texture_count_size_7.y));}
    else {color = vec4(1.0, 0.0, 0.0, 1.0);}

    fragColor = color;
}