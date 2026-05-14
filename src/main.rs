#![allow(unused)]

mod chip8;

use std::{
    thread,
    time
};
use std::time::Duration;
use std::io::{
    stdout,
    Result
};
use crossterm::{
    execute,
    cursor
}; 
use crossterm::style::Print;
use crossterm::terminal::{
    Clear,
    ClearType,
    disable_raw_mode,
    enable_raw_mode,
    EnterAlternateScreen,
    LeaveAlternateScreen,
};
use crossterm::event::{
    read,
    poll,
    Event,
    KeyCode,
    KeyEventKind,
    KeyboardEnhancementFlags,
    PushKeyboardEnhancementFlags,
    PopKeyboardEnhancementFlags
};

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
    let cycles_per_frame = 8;
    const WAIT_TIME: Duration = time::Duration::from_millis(1);
    const WAIT_TIME_2: Duration = time::Duration::from_millis(1);

    loop {
        if poll(WAIT_TIME_2).unwrap() {
            let event = read()?;

            match event {
                Event::Key(event) => {
                    match event.kind {
                        KeyEventKind::Press => {
                            match event.code {
                                KeyCode::Char('1') => chip.key[0x1] = true,
                                KeyCode::Char('2') => chip.key[0x2] = true,
                                KeyCode::Char('3') => chip.key[0x3] = true,
                                KeyCode::Char('4') => chip.key[0xC] = true,
                                KeyCode::Char('q') => chip.key[0x4] = true,
                                KeyCode::Char('w') => chip.key[0x5] = true,
                                KeyCode::Char('e') => chip.key[0x6] = true,
                                KeyCode::Char('r') => chip.key[0xD] = true,
                                KeyCode::Char('a') => chip.key[0x7] = true,
                                KeyCode::Char('s') => chip.key[0x8] = true,
                                KeyCode::Char('d') => chip.key[0x9] = true,
                                KeyCode::Char('f') => chip.key[0xE] = true,
                                KeyCode::Char('z') => chip.key[0xA] = true,
                                KeyCode::Char('x') => chip.key[0x0] = true,
                                KeyCode::Char('c') => chip.key[0xB] = true,
                                KeyCode::Char('v') => chip.key[0xF] = true,
                                KeyCode::Esc => break,
                                _ => {},
                            }
                        },
                        KeyEventKind::Release => {
                            match event.code {
                                KeyCode::Char('1') => chip.key[0x1] = false,
                                KeyCode::Char('2') => chip.key[0x2] = false,
                                KeyCode::Char('3') => chip.key[0x3] = false,
                                KeyCode::Char('4') => chip.key[0xC] = false,
                                KeyCode::Char('q') => chip.key[0x4] = false,
                                KeyCode::Char('w') => chip.key[0x5] = false,
                                KeyCode::Char('e') => chip.key[0x6] = false,
                                KeyCode::Char('r') => chip.key[0xD] = false,
                                KeyCode::Char('a') => chip.key[0x7] = false,
                                KeyCode::Char('s') => chip.key[0x8] = false,
                                KeyCode::Char('d') => chip.key[0x9] = false,
                                KeyCode::Char('f') => chip.key[0xE] = false,
                                KeyCode::Char('z') => chip.key[0xA] = false,
                                KeyCode::Char('x') => chip.key[0x0] = false,
                                KeyCode::Char('c') => chip.key[0xB] = false,
                                KeyCode::Char('v') => chip.key[0xF] = false,
                                _ => {},
                            }
                        },
                        _ => {},
                    }
                }
                _ => {}
            }
        }

        for _ in 0..cycles_per_frame {
            chip.emulate_cycle();
        }

        if chip.sound_timer > 0 {
            print!("{}", 0x07 as char);
        }

        if chip.should_draw {
            execute!(stdout(),
                Clear(ClearType::All),
                cursor::MoveTo(0, 0),
            )?;

            for y in 0..32 {
                for x in 0..64 {
                    if chip.gfx[x + y * 64] == 1 {
                        print_crossterm(x, y);
                    }
                }
            }

            chip.should_draw = false;
        }

        thread::sleep(WAIT_TIME);
    }
    Ok(())
}

fn print_crossterm(x: usize, y: usize) -> Result<()> {
    execute!(
        stdout(),
        cursor::MoveTo(x as u16, y as u16),
        Print("█"),
    )?;

    Ok(())
}

fn main() {
    let rom = 7;

    match rom {
        1 => test_rom_1(),
        2 => test_rom_2(),
        3 => test_rom_3(),
        4 => test_rom_4(),
        5 => test_rom("roms/5-quirks.ch8").expect("something went wrong"),
        6 => test_rom("roms/6-keypad.ch8").expect("something went wrong"),
        7 => test_rom("roms/7-beep.ch8").expect("something went wrong"),
        8 => test_rom("roms/pong.ch8").expect("something went wrong"),
        _ => panic!("test rom does not exist!"),
    }
}
