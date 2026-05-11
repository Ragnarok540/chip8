pub struct Chip8 {
    pub opcode: usize,
    memory: [usize; 4096],
    gfx: [u8; 64 * 32], // graphics
    v: [usize; 16],     // registers
    i: usize,           // index
    pc: usize,          // program counter
    delay_timer: u8,
    sound_timer: u8,
    stack: [usize; 16],
    sp: usize,          // stack pointer
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

    fn vxi(&self) -> usize {
        (self.opcode & 0x0F00) >> 8
    }

    fn vyi(&self) -> usize {
        (self.opcode & 0x00F0) >> 4
    }

    fn n(&self) -> usize {
        self.opcode & 0x000F
    }

    fn nn(&self) -> usize {
        self.opcode & 0x00FF
    }

    fn nnn(&self) -> usize {
        self.opcode & 0x0FFF
    }

    pub fn load_rom(&mut self, path: &str) {
        let bytes = std::fs::read(path).unwrap();
        let mut counter = 0;

        for byte in bytes.chunks_exact(1) {
            self.memory[self.pc + counter] = byte[0] as usize;
            counter += 1;
        }
    }

    pub fn emulate_cycle(&mut self) {
        self.fetch_opcode();
        self.pc += 2;
        self.decode_opcode();
    }

    pub fn draw_console(&self) {
        for y in 0..32 {
            for x in 0..64 {
                if self.gfx[x + y * 64] == 1 {
                    print!("█");
                } else {
                    print!(" ");
                }
                if x == 63 {
                    println!();
                }
            }
        } 
    }

    fn fetch_opcode(&mut self) {
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1];
    }

    fn decode_opcode(&mut self) {
        match self.opcode & 0xF000 {
            0x000 => {
                match self.opcode & 0x00FF {
                    0x00E0 => self.clear_screen(),
                    0x00EE => self.ret(),
                    _ => panic!("opcode could not be decoded: {0:#x}", self.opcode),
                }
            },
            0x1000 => self.goto(),
            0x2000 => self.call(),
            0x3000 => self.skip_equal(),
            0x4000 => self.skip_not_equal(),
            0x5000 => self.skip_equal_reg(),
            0x6000 => self.load_reg(),
            0x7000 => self.add_constant(),
            0x8000 => {
                match self.opcode & 0x000F {
                    0x0000 => self.set_reg(),
                    0x0001 => self.bitwise_or(),
                    0x0002 => self.bitwise_and(),
                    0x0003 => self.bitwise_xor(),
                    0x0004 => self.add(),
                    0x0005 => self.sub(),
                    0x0006 => self.shr(),
                    0x0007 => self.subn(),
                    0x000E => self.shl(),
                    _ => panic!("opcode could not be decoded: {0:#x}", self.opcode),
                }
            },
            0x9000 => self.skip_reg_not_equal(),
            0xA000 => self.load_index(),
            0xB000 => println!("jump"),
            0xC000 => println!("random_value"),
            0xD000 => self.draw(),
            0xE000 => {
                match self.opcode & 0x00FF {
                    0x009E => println!("skip_key_pressed"),
                    0x00A1 => println!("skip_key_not_pressed"),
                    _ => panic!("opcode could not be decoded: {0:#x}", self.opcode),
                }
            },
            0xF000 => {
                match self.opcode & 0x00FF {
                    0x0007 => println!("load_delay"),
                    0x000A => println!("load_key_pressed"),
                    0x0015 => println!("set_delay"),
                    0x0018 => println!("set_sound"),
                    0x001E => self.add_index(),
                    0x0029 => println!("load_hex_sprite"),
                    0x0033 => self.store_bcd(),
                    0x0055 => self.store_regs(),
                    0x0065 => self.read_regs(),
                    _ => panic!("opcode could not be decoded: {0:#x}", self.opcode),
                }
            },
            _ => panic!("opcode could not be decoded: {0:#x}", self.opcode),
        }
    }

    // 00E0 TESTED
    fn clear_screen(&mut self) {
        self.gfx = [0; 64 * 32];
    }

    // 00EE TESTED
    fn ret(&mut self) {
        self.sp -= 1;
        self.pc = self.stack[self.sp];
    }

    // 1NNN TESTED
    fn goto(&mut self) {
        self.pc = self.nnn();
    }

    // 2NNN TESTED
    fn call(&mut self) {
        self.stack[self.sp] = self.pc;
        self.sp += 1;
        self.pc = self.nnn();
    }

    // 3XNN TESTED
    fn skip_equal(&mut self) {
        if self.v[self.vxi()] == self.nn() {
            self.pc += 2;
        }
    }

    // 4XNN TESTED
    fn skip_not_equal(&mut self) {
        if self.v[self.vxi()] != self.nn() {
            self.pc += 2;
        }
    }

    // 5XY0 TESTED
    fn skip_equal_reg(&mut self) {
        if self.v[self.vxi()] == self.v[self.vyi()] {
            self.pc += 2;
        }
    }

    // 6XNN TESTED
    fn load_reg(&mut self) {
        self.v[self.vxi()] = self.nn();
    }

    // 7XNN TESTED
    fn add_constant(&mut self) {
        let val = self.v[self.vxi()] + self.nn();
        self.v[self.vxi()] = val & 0xFF;
    }

    // 8XY0 TESTED
    fn set_reg(&mut self) {
        self.v[self.vxi()] = self.v[self.vyi()];
    }

    // 8XY1 TESTED
    fn bitwise_or(&mut self) {
        self.v[self.vxi()] = self.v[self.vxi()] | self.v[self.vyi()];
    }

    // 8XY2 TESTED
    fn bitwise_and(&mut self) {
        self.v[self.vxi()] = self.v[self.vxi()] & self.v[self.vyi()];
    }

    // 8XY3 TESTED
    fn bitwise_xor(&mut self) {
        self.v[self.vxi()] = self.v[self.vxi()] ^ self.v[self.vyi()];
    }

    // 8XY4
    fn add(&mut self) {
        let val = self.v[self.vxi()] + self.v[self.vyi()];
        self.v[self.vxi()] = val & 0xFF;

        if val > 0xFF {
            self.v[0xF] = 0x1;
        } else {
            self.v[0xF] = 0x0;
        }           
    }

    // 8XY5 TESTED
    fn sub(&mut self) {
        let val_0 = self.v[self.vxi()];
        let val_1 = self.v[self.vxi()] as isize - self.v[self.vyi()] as isize;
        self.v[self.vxi()] = val_1 as usize & 0xFF;

        if val_0 >= self.v[self.vyi()] {
            self.v[0xF] = 0x1;
        } else {
            self.v[0xF] = 0x0;
        }
    }

    // 8XY6 TESTED
    fn shr(&mut self) {
        let val = self.v[self.vxi()];
        self.v[self.vxi()] = (self.v[self.vxi()] >> 1) & 0xFF;
        self.v[0xF] = val & 0x1;
    }

    // 8XY7 TESTED
    fn subn(&mut self) {
        let val = self.v[self.vyi()] as isize - self.v[self.vxi()] as isize;
        self.v[self.vxi()] = val as usize & 0xFF;

        if self.v[self.vyi()] > self.v[self.vxi()] {
            self.v[0xF] = 0x1;
        } else {
            self.v[0xF] = 0x0;
        }  
    }

    // 8XYE TESTED
    fn shl(&mut self) {
        let val = self.v[self.vxi()];
        self.v[self.vxi()] = (self.v[self.vxi()] << 1) & 0xFF;
        self.v[0xF] = (val & 0x80) >> 7;
    }

    // 9XY0 TESTED
    fn skip_reg_not_equal(&mut self) {
        if self.v[self.vxi()] != self.v[self.vyi()] {
            self.pc += 2;
        } 
    }

    // ANNN TESTED
    fn load_index(&mut self) {
        self.i = self.nnn();
    }

    // DXYN TESTED
    fn draw(&mut self) {
        let x_pos = self.v[self.vxi()] % 64;
        let y_pos = self.v[self.vyi()] % 32;
        let height = self.n();
        self.v[0xF] = 0;

        for row in 0..height {
            let pixel = self.memory[self.i + row];

            for col in 0..8 {
                if (pixel & (0x80 >> col)) != 0 {
                    let pix = x_pos + col + ((y_pos + row) * 64);

                    if self.gfx[pix % 2048] == 1 {
                        self.v[0xF] = 1;
                    }

                    self.gfx[pix % 2048] ^= 1;
                }
            }
        }
    }

    // FX1E TESTED
    fn add_index(&mut self) {
        self.i = self.i + self.v[self.vxi()];
    }

    // FX33 TESTED
    fn store_bcd(&mut self) {
        let hundred = self.v[self.vxi()] / 100 % 10;
        let ten = self.v[self.vxi()] / 10 % 10;
        let one = self.v[self.vxi()] % 10;

        self.memory[self.i] = hundred;
        self.memory[self.i + 1] = ten;
        self.memory[self.i + 2] = one;
    }

    // FX55 TESTED
    fn store_regs(&mut self) {
        for i in 0..(self.vxi() + 1) {
            self.memory[self.i + i] = self.v[i];
        }
    }

    // FX65 TESTED
    fn read_regs(&mut self) {
        for i in 0..(self.vxi() + 1) {
            self.v[i] = self.memory[self.i + i];
        }
    }
}
