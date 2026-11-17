// Box.asm for Roll No: 2501010072 (K = 72)
// Start Row = 72 -> Address = 16384 + (32 * 72) = 18688
// Height = 20 rows
// Width = ((72 mod 4) + 1) = 1 word (16 pixels) wide from left edge

(MAIN_LOOP)
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE       // If KBD != 0, key is pressed -> draw black (-1)

    @color
    M=0         // Key is released -> draw white (0)
    @DRAW_BOX
    0;JMP

(KEY_PRESSED)
    @color
    M=-1        // -1 = 1111111111111111 in binary (16 black pixels)

(DRAW_BOX)
    @18688      // SCREEN (16384) + 32 * 72 = 18688
    D=A
    @rowAddr
    M=D

    @20         // Box height = 20 rows
    D=A
    @rowsLeft
    M=D

(ROW_LOOP)
    @rowsLeft
    D=M
    @MAIN_LOOP
    D;JLE       // If rowsLeft <= 0, return to MAIN_LOOP

    @rowAddr
    D=M
    @currWord
    M=D

    @1          // Box width = (72 mod 4) + 1 = 1 word (16 pixels)
    D=A
    @colsLeft
    M=D

(COL_LOOP)
    @colsLeft
    D=M
    @NEXT_ROW
    D;JLE       // Finished 1 word in current row -> jump to NEXT_ROW

    @color
    D=M
    @currWord
    A=M         // Point A to screen memory word
    M=D         // Fill 16 pixels with color

    @currWord
    M=M+1       // Move 1 word (16 pixels) right
    @colsLeft
    M=M-1
    @COL_LOOP
    0;JMP

(NEXT_ROW)
    @32
    D=A
    @rowAddr
    M=D+M       // Advance down 1 row (+32 words)
    @rowsLeft
    M=M-1
    @ROW_LOOP
    0;JMP