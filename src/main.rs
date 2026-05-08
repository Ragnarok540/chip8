mod chip8;

use crate::chip8::Chip8;

fn main() {
    println!("hello world");

    let mut chip = Chip8::new();
    chip.opcode = 0x000E;
    // let vxi = 
    chip.decode_opcode();
    // println!("{vxi:#x}");
    // println!("{vxi}");
}
