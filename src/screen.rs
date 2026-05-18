use crossterm::{
    execute,
    cursor
}; 
use crossterm::style::Print;
use crossterm::terminal::{
    Clear,
    ClearType,
};

use std::io::{
    stdout
};

use crate::chip8::Chip8;

pub fn draw_screen(chip: &mut Chip8) {
    if chip.should_draw {
        execute!(stdout(),
            Clear(ClearType::All),
            cursor::MoveTo(0, 0),
        );

        for y in 0..32 {
            for x in 0..64 {
                if chip.gfx[x + y * 64] == 1 {
                    execute!(stdout(),
                        cursor::MoveTo(x as u16, y as u16),
                        Print("█"),
                    );
                }
            }
        }
        chip.should_draw = false;
    }

}
