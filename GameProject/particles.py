import pygame
from support import import_folder
from random import choice


def reflect_images(frames, x, y):
    new_frames = []

    for frame in frames:
        flipped_frame = pygame.transform.flip(frame, x, y)
        new_frames.append(flipped_frame)

    return new_frames

def rotate_images(frames):
    new_frames = []

    for frame in frames:
        rotated_frame = pygame.transform.rotate(frame, 90)
        new_frames.append(rotated_frame)

    return new_frames


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'heal_bubbles': import_folder('images/particles/heal_bubbles'),
            'heal': import_folder('images/particles/heal'),
            'ball_1': import_folder('images/particles/ball_1'),
            'ball_2': import_folder('images/particles/ball_2'),
            'ball_3': import_folder('images/particles/ball_3'),
            'ball_4': import_folder('images/particles/ball_4'),
            'ball_5': import_folder('images/particles/ball_5'),
            'ball_6': import_folder('images/particles/ball_6'),
            'ball_impulse': import_folder('images/particles/ball_impulse'),
            'tentacles': import_folder('images/particles/tentacles'),

            # attacks
            'dark_eye': import_folder('images/particles/dark_eye'),
            'bite': reflect_images(import_folder('images/particles/bite'), 1, 0),
            'goo': import_folder('images/particles/goo'),

            # enemy deaths
            'bat': import_folder('images/particles/deaths/bat'),
            'jaws': import_folder('images/particles/deaths/jaws'),
            'poo': import_folder('images/particles/deaths/poo'),

            # grass
            'grass': (import_folder('images/particles/grass'),
                      import_folder('images/particles/grass_1'),
                      reflect_images(import_folder('images/particles/grass'), 1, 0),
                      reflect_images(import_folder('images/particles/grass_1'), 1, 0))
        }

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['grass'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        if 'up' in animation_type:
            animation_frames = rotate_images(self.frames[animation_type[0:-3]])
        elif 'down' in animation_type:
            animation_frames = reflect_images(rotate_images(self.frames[animation_type[0:-5]]), 0, 1)
        elif 'left' in animation_type:
            animation_frames = reflect_images(self.frames[animation_type[0:-5]], 1, 0)
        else:
            animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.sprite_type = 'magic'

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
