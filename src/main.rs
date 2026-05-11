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

fn test_rom_3() {
    let mut chip = Chip8::new();
    chip.load_rom("roms/3-corax+.ch8");

    for _ in 0..307 {
        chip.emulate_cycle();
    }

    chip.draw_console();
}

fn test_rom_4() {
    let mut chip = Chip8::new();
    chip.load_rom("roms/4-flags.ch8");

    for _ in 0..960 {
        chip.emulate_cycle();
    }

    chip.draw_console();
}


fn main() {
    let test_rom = 4;

    match test_rom {
        1 => test_rom_1(),
        2 => test_rom_2(),
        3 => test_rom_3(),
        4 => test_rom_4(),
        _ => panic!("test rom does not exist!"),
    }
}
