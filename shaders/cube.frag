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

void main() {
    vec3 color = vec3(face_0/5.0, 0.0, 0.0);

    if(face_0 == 0.0) {color = texture(u_texture_0, uv_0).rgb;}
    else if(face_0 == 1.0) {color = texture(u_texture_1, uv_0).rgb;}
    else if(face_0 == 2.0) {color = texture(u_texture_2, uv_0).rgb;}
    else if(face_0 == 3.0) {color = texture(u_texture_3, uv_0).rgb;}
    else if(face_0 == 4.0) {color = texture(u_texture_4, uv_0).rgb;}
    else {color = texture(u_texture_5, uv_0).rgb;}

    fragColor = vec4(color, 1.0);
}