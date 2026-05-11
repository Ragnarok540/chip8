#![allow(unused)]

mod chip8;

use crate::chip8::Chip8;

fn test_rom_1() {
    let mut chip = Chip8::new();
    chip.load_rom("roms/1-chip8-logo.ch8");

    for _ in 0..40 {
        chip.emulate_cycle();
    }

    chip.draw_console();
}

fn test_rom_2() {
    let mut chip = Chip8::new();
    chip.load_rom("roms/2-ibm-logo.ch8");

    for _ in 0..21 {
        chip.emulate_cycle();
    }

    chip.draw_console();
}

fn main() {
    let test_rom = 2;

    match test_rom {
        1 => rom1(),
        2 => rom2(),
        _ => panic!("test rom does not exist!"),
    }

}
