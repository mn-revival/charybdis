; This file is used to test full coverage of all GB instructions.
; Eventually we'll run an automated test against this.

SECTION "ROM Bank $000", ROM0[$150]

;;;;;;;;;;;
; LD r, r ;
;;;;;;;;;;;

; LD B, r
ld B, B
ld B, C
ld B, D
ld B, E
ld B, H
ld B, L
ld B, [HL]
ld B, A

; LD C, r
ld C, B
ld C, C
ld C, D
ld C, E
ld C, H
ld C, L
ld C, [HL]
ld C, A

; LD D, r
ld D, B
ld D, C
ld D, D
ld D, E
ld D, H
ld D, L
ld D, [HL]
ld D, A

; LD E, r
ld E, B
ld E, C
ld E, D
ld E, E
ld E, H
ld E, L
ld E, [HL]
ld E, A

; LD H, r
ld H, B
ld H, C
ld H, D
ld H, E
ld H, H
ld H, L
ld H, [HL]
ld H, A

; LD L, r
ld L, B
ld L, C
ld L, D
ld L, E
ld L, H
ld L, L
ld L, [HL]
ld L, A

; LD [HL], r
ld [HL], B
ld [HL], C
ld [HL], D
ld [HL], E
ld [HL], H
ld [HL], L
ld [HL], A

ld A, B
ld A, C
ld A, D
ld A, E
ld A, H
ld A, L
ld A, [HL]
ld A, A

; LD r, n ; load immediate to register
ld B, $f0
ld C, $f1
ld D, $f2
ld E, $f3
ld H, $f4
ld L, $f5
ld [HL], $f6
ld A, $f7

; Load accumulator/indirect 16 bit
ld A, [BC]
ld A, [DE]
ld [BC], A
ld [DE], A

; Load accumulator/direct
ld A, [$f0]
ld [$f0], A

; Load accumulator/indirect 8 bit
ldh A, [C]
ldh [C], A

; load indirect, increment/decrement
ld A, [HL-]
ld [HL-], A
ld A, [HL+]
ld [HL+], A
