#![allow(unused)]

mod chip8;

use crate::chip8::Chip8;

fn main() {
    let mut chip = Chip8::new();
    chip.load_rom("roms/1-chip8-logo.ch8");

    for _ in 0..40 {
        chip.emulate_cycle();
    }

    chip.draw_console();
}
