flag = "KCTF_Jr{T0o_M4nY_f4nCt10N5_5Ut_f1Nd_EnTrY_P01nT_4nd_s0_e45y_1og1C}"
expected = [((ord(f) ^ 0x55) + 5) for f in flag]
print(', '.join([f"0x{c:x}" for c in expected]))

