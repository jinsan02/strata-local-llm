<tool_call>
<function=edit_file>
<parameter=path_glob>
src/packaging/specifiers.py
</parameter>
<parameter=search>
        return VersionRange._from_specifier_set(self)

    def _check_relation_operand(self, other: object) -> None:
</parameter>
<parameter=new>
        return VersionRange._from_specifier_set(self)

    def bounds(self) -> tuple[None | tuple[Version, bool], None | tuple[Version, bool]]:
        """Return the combined lower and upper bounds of this specifier set."""
        if not self._specs:
            return (None, None)
            
        if any(s.operator == "===" for s in self._specs):
            raise ValueError("bounds() does not support === specifiers")
            
        lower_candidates: list[tuple[Version, bool]] = []
        upper_candidates: list[tuple[Version, bool]] = []
        
        for spec in self._specs:
            op, ver_str = spec._spec
            v = spec.version
            
            if op == ">=":
                lower_candidates.append((v, True))
            elif op == ">":
                lower_candidates.append((v, False))
            elif op == "<=":
                upper_candidates.append((v, True))
            elif op == "<":
                upper_candidates.append((v, False))
            elif op == "==":
                if ver_str.endswith(".*"):
                    lower_candidates.append((v, True))
                    rel = v.release[:-1] + (v.release[-1] + 1,)
                    ep_str = f"{v.epoch}!" if v.epoch > 0 else ""
                    u_ver = Version(f"{ep_str}{'.'.join(map(str, rel))}")
                    upper_candidates.append((u_ver, False))
                else:
                    lower_candidates.append((v, True))
                    upper_candidates.append((v, True))
            elif op == "~=":
                lower_candidates.append((v, True))
                rel = v.release[:-2] + (v.release[-1] + 1,)
                ep_str = f"{v.epoch}!" if v.epoch > 0 else ""
                u_ver = Version(f"{ep_str}{'.'.join(map(str, rel))}")
                upper_candidates.append((u_ver, False))
                
        lower: tuple[Version, bool] | None = None
        if lower_candidates:
            lower = max(lower_candidates, key=lambda b: (b[0], not b[1]))
            
        upper: tuple[Version, bool] | None = None
        if upper_candidates:
            upper = min(upper_candidates, key=lambda b: (b[0], b[1]))
            
        return (lower, upper)

    def _check_relation_operand(self, other: object) -> None:
</parameter>
</function>
</tool_call>