#![allow(unused)]

mod chip8;
mod keypad;
mod screen;

use std::time::{
    Duration,
    SystemTime,
};
use std::io::{
    stdout,
    Result
};

use crossterm::{
    execute,
    cursor,
}; 
use crossterm::terminal::{
    disable_raw_mode,
    enable_raw_mode,
    EnterAlternateScreen,
    LeaveAlternateScreen,
};
use crossterm::event::{
    KeyboardEnhancementFlags,
    PushKeyboardEnhancementFlags,
    PopKeyboardEnhancementFlags,
};

use crate::chip8::Chip8;
use crate::keypad::handle_keypad;
use crate::screen::draw;

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

fn test_rom(path: &str) -> Result<()>  {
    let mut chip = Chip8::new();
    chip.load_rom(path);

    execute!(stdout(),
        EnterAlternateScreen,
        PushKeyboardEnhancementFlags(KeyboardEnhancementFlags::REPORT_EVENT_TYPES),
        cursor::Hide,
    )?;

    enable_raw_mode()?;

    if let Err(e) = chip8_loop(&mut chip) {
        eprintln!("Error: {:?}\r", e);
    }

    disable_raw_mode()?;

    execute!(stdout(),
        cursor::Show,
        PopKeyboardEnhancementFlags,
        LeaveAlternateScreen,
    )?;

    Ok(())
}

fn chip8_loop(chip: &mut Chip8) -> Result<()> {
    let mut last_time = SystemTime::now();
    let mut not_processed = 0.0;
    const NS_PER_CYCLE: f64 = 1000000000.0 / 480.0;

    loop {
        if let Some(esc) = handle_keypad(chip) {
            if esc {
                break;
            }
        }

        let now = SystemTime::now();
        let difference = now.duration_since(last_time).expect("Clock may have gone backwards");
        not_processed += (difference.as_nanos() as f64) / NS_PER_CYCLE;
        last_time = now;

        while not_processed >= 1.0 {
            chip.emulate_cycle();
            not_processed -= 1.0;
        }

        if chip.sound_timer > 0 {
            print!("{}", 0x07 as char);
        }

        if chip.draw_flag {
            draw(chip);
        }

    }
    Ok(())
}

fn main() {
    let rom = 6;

    match rom {
        1 => test_rom_1(),
        2 => test_rom_2(),
        3 => test_rom_3(),
        4 => test_rom_4(),
        5 => test_rom("roms/5-quirks.ch8").expect("something went wrong"),
        6 => test_rom("roms/6-keypad.ch8").expect("something went wrong"),
        7 => test_rom("roms/7-beep.ch8").expect("something went wrong"),
        8 => test_rom("roms/pong.ch8").expect("something went wrong"),
        9 => test_rom("roms/invaders.ch8").expect("something went wrong"),
        _ => panic!("test rom does not exist!"),
    }
}
