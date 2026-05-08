pub struct Chip8 {
    pub opcode: u16,
    memory: [u8; 4096],
    gfx: [u8; 64 * 32], // graphics
    v: [u8; 16],        // registers
    i: u16,             // index
    pc: u16,            // program counter
    delay_timer: u8,
    sound_timer: u8,
    stack: [u8; 16],
    sp: u8,             // stack pointer
    key: [u8; 16],
}

impl Chip8 {
    pub fn new() -> Self {
        Self {
            opcode: 0,
            memory: [0; 4096],
            gfx: [0; 64 * 32],
            v: [0; 16],
            i: 0,
            pc: 0x200,
            delay_timer: 0,
            sound_timer: 0,
            stack: [0; 16],
            sp: 0,
            key: [0; 16],
        }
    }

    fn vxi(&self) -> u16 {
        (self.opcode & 0x0F00) >> 8
    }

    fn vyi(&self) -> u16 {
        (self.opcode & 0x00F0) >> 4
    }

    fn n(&self) -> u16 {
        self.opcode & 0x000F
    }

    fn nn(&self) -> u16 {
        self.opcode & 0x00FF
    }

    fn nnn(&self) -> u16 {
        self.opcode & 0x0FFF
    }

    pub fn decode_opcode(&self) {
        match self.opcode & 0xF000 {
            0x000 => {
                match self.opcode & 0x00FF {
                    0x00E0 => println!("clear_screen"),
                    0x00EE => println!("ret"),
                    _ => panic!("decode error: {0:#x}", self.opcode),
                }
            },
            _ => panic!("decode error: {0:#x}", self.opcode),
        }
    }
}
