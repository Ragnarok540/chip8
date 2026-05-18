use crate::chip8::Chip8;

use std::time::Duration;

use crossterm::event::{
    read,
    poll,
    Event,
    KeyCode,
    KeyEventKind,
};

pub fn handle_keypad(chip: &mut Chip8) -> Option<bool> {
    const WAIT_TIME: Duration = Duration::from_millis(1);

    if poll(WAIT_TIME).unwrap() {
        let event = read().ok()?;
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
                            KeyCode::Esc => return Some(true),
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
    return Some(false);
}
