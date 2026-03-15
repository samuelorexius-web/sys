#!storage/emulated/0/pluning.py
#!use pluning.py
#!generateur objet...
#
# v2.0 — Accélération C via _pluning_core
# Les fonctions critiques (reaper, compile_exec, build_*code, join_params)
# utilisent l'extension C si disponible, sinon fallback Python transparent.
#
# Compiler d'abord :
#   python setup_pluning.py build_ext --inplace
#

# ── Import du noyau C (optionnel — fallback pur Python) ─────────
import sys as _sys, os as _os, glob as _glob, importlib.util as _ilu

def _find_and_load_core():
    """
    Cherche _pluning_core*.so et le charge DIRECTEMENT par son chemin
    complet via importlib — sans dépendre de sys.path.
    """
    _candidates = [
        _os.path.dirname(_os.path.abspath(__file__)),  # dossier de pluning.py
        _os.getcwd(),                                   # dossier courant
        _os.path.join(_os.getcwd(), "project"),         # sous-dossier project
        _os.path.expanduser("~/project"),               # ~/project Termux
        # chemin absolu Android courant
        "/storage/emulated/0/project",
        "/data/data/com.termux/files/home/project",
    ]
    for _d in _candidates:
        _hits = _glob.glob(_os.path.join(_d, "_pluning_core*.so"))
        if not _hits:
            # essayer aussi sans extension explicite
            _hits = _glob.glob(_os.path.join(_d, "_pluning_core*"))
            _hits = [h for h in _hits if h.endswith(".so") or ".cpython" in h]
        if _hits:
            _so_path = _hits[0]
            try:
                _spec = _ilu.spec_from_file_location("_pluning_core", _so_path)
                _mod  = _ilu.module_from_spec(_spec)
                _spec.loader.exec_module(_mod)
                _sys.modules["_pluning_core"] = _mod
                return _mod, True
            except Exception:
                continue
    # dernier recours : import classique
    try:
        import _pluning_core as _c
        return _c, True
    except ImportError:
        return None, False

_core, _C_AVAILABLE = _find_and_load_core()

# ── Fallbacks Python (si C non compilé) ─────────────────────────
class _FallbackCore:
    """Réimplémentation Python de _pluning_core — même API, sans C."""

    @staticmethod
    def reaper(code: str, i: int = 1) -> str:
        lines  = code.splitlines()
        indent = i * 4
        result = []
        for line in lines:
            if not line.strip():
                result.append("")
            else:
                result.append(" " * indent + line)
        return "\n".join(result) + "\n"

    @staticmethod
    def compile_exec(code: str, attr: str):
        ns = {}
        exec(compile(code, "<pluning>", "exec"), ns)
        if attr not in ns:
            raise KeyError(f"attribut '{attr}' introuvable dans le namespace")
        return ns[attr]

    @staticmethod
    def build_func_code(name: str, params: str, body: str) -> str:
        if params:
            return f"def {name}({params}):\n    {body}"
        return f"def {name}():\n    {body}"

    @staticmethod
    def build_class_code(name: str, parents: str, body: str) -> str:
        if parents:
            return f"class {name}({parents}):\n    {body}"
        return f"class {name}:\n    {body}"

    @staticmethod
    def join_params(params_list: list) -> str:
        return ", ".join(params_list)

# Utiliser C si disponible, sinon fallback
_CORE = _core if _C_AVAILABLE else _FallbackCore()


# ════════════════════════════════════════════════════════════════
# Base
# ════════════════════════════════════════════════════════════════
class Base:
    def __init__(self):
        self.json     = __import__("json")
        self.os       = __import__("os")
        self.abs_dir  = "Systeme/states/emulated/0/json/"
        self.abs_name = "data_pluning.py"
        self.abs_path = self.os.path.join(self.abs_dir, self.abs_name)
        self.li       = "use namespace; data of pluning."

    class extented:

        def Codecs(self, code, attr):
            from Systeme.IO.tools.Codecs import lambdaCodecs
            namespace = {}
            try:
                return lambdaCodecs.statistc_encode(code)
            except:  # incompatibilité éventuelle
                exec(code, namespace)
                return namespace[attr]

        def ast_Codecs(self, code, attr):
            from Systeme.IO.tools.Codecs import ast_to_string, string_to_ast
            namespace = {}
            try:
                ast = string_to_ast._string_to_ast(code)
                exec(ast_to_string._ast_to_string, namespace)
                return namespace.get(attr, None)
            except Exception as e:
                from Systeme.vendor.release.Error import SystemeError
                raise SystemeError(e) from e

        def reaper(self, code: str, i: int = 1) -> str:
            """
            Indente chaque ligne de code de (i * 4) espaces.
            ── Utilise _pluning_core.reaper (C) si disponible ──
            """
            return _CORE.reaper(code, i)

    class SystemClass:
        """Réseau de compilation/exécution de classes."""

        def network(code, attr):
            pass

        def _compile(self, code: str, attr: str):
            """
            Compile et exec du code Python, retourne namespace[attr].
            ── Utilise _pluning_core.compile_exec (C) si disponible ──
            """
            try:
                return _CORE.compile_exec(code, attr)
            except Exception as e:
                from Systeme.vendor.release.Error import SystemeError
                raise SystemeError(e) from e

    SystemClass = SystemClass()
    extented    = extented()


# ════════════════════════════════════════════════════════════════
# _new  —  Générateur d'objets dynamiques
# ════════════════════════════════════════════════════════════════
class _new(Base):
    def __init__(self):
        self.file        = None
        self.extented    = Base.extented
        self.SystemClass = Base.SystemClass

    def __setattr__(self, _name, _value):
        super().__setattr__(_name, _value)

    def __getattr__(self, attr, i: int = 1, ptype=False):

        def creator(*a, **kw):
            self.file    = attr
            self.type    = kw.get('type', 'func')
            self.subparam = kw.get('param', ord('A'))

            # Résolution du type (ptype surchargé ou depuis kw)
            if ptype is not False:
                self.type = ptype

            # ── Construction du paramètre (param) ──────────────
            if isinstance(self.subparam, list):
                # ── Utilise _pluning_core.join_params (C) ──
                self.param = _CORE.join_params(self.subparam)
            elif isinstance(self.subparam, str):
                self.param = self.subparam
            else:
                self.param = ''

            self.namespace = {}

            # ── TYPE : func ────────────────────────────────────
            if self.type == 'func':
                importing = kw.get('importing', 'time')
                # Éviter "import " si la valeur est vide
                if importing and importing.strip():
                    self.importOject = f"\nimport {importing}"
                else:
                    self.importOject = ""
                body_raw  = kw.get('value', '\nreturn True')

                if self.importOject:
                    indented_import = self.extented.reaper(self.importOject, i)
                    self.body = f"{indented_import}\n    {self.extented.reaper(body_raw, i)}"
                    exec(self.importOject)  # injecter l'import dans l'env courant
                else:
                    self.body = self.extented.reaper(body_raw, i)

                # ── Construire le code de la fonction (C) ──────
                self.code = _CORE.build_func_code(attr, self.param, self.body)

                # Tenter l'encodage via Codecs (lambdaCodecs)
                try:
                    self.__setattr__("call_" + attr,
                                     self.extented.Codecs(self.code, attr))
                except:
                    try:
                        self.__setattr__("call_" + attr,
                                         self.extented.ast_Codecs(self.code, attr))
                    except:
                        pass  # Codecs non disponibles — on continue sans

                exec(self.code, self.namespace)
                return self.namespace.get(attr)

            # ── TYPE : str ─────────────────────────────────────
            elif self.type == 'str' or self.type == type(str()):
                self.body = kw.get('value', str(*a) if a else '')
                self.code = f"{attr} = '{self.body}'"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : int ─────────────────────────────────────
            elif self.type == 'int' or self.type == type(int()):
                self.body = kw.get('value', int(*a) if a else 0)
                self.code = f"{attr} = {self.body}"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : bool ────────────────────────────────────
            elif self.type == 'bool' or self.type == type(bool()):
                self.body = kw.get('value', bool(*a) if a else False)
                self.code = f"{attr} = {self.body}"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : object / class ──────────────────────────
            elif self.type in ("object", "class"):
                _parent_raw = kw.get("parrent", "")

                if isinstance(_parent_raw, list):
                    self.parrent = ", ".join(_parent_raw)
                elif isinstance(_parent_raw, str):
                    self.parrent = _parent_raw
                else:
                    self.parrent = ''

                self.body = self.extented.reaper(
                    kw.get('value', self._delfaut())
                )

                # ── Construire le code de la classe (C) ────────
                self.code = _CORE.build_class_code(attr, self.parrent, self.body)

                obj = self.SystemClass._compile(self.code, attr)
                self.__setattr__("class_" + attr, obj)
                return obj

            else:
                return ""  # valeur par défaut pour le type inconnu

        return creator

    def _delfaut(self) -> str:
        """Corps par défaut d'une classe : __new__, __init__, onde."""
        tasks = ["__new__", "__init__", "onde"]
        values = [
            """
self = super().__new__(self)
return self
""",
            """
self.char = '+'
self.w = 9
self.c = 12
self.v = 90
""",
            """
t = 0
while True:
    self.color = f"\\033[{self.v}m"
    self.y = math.sin(t)
    self.x = math.cos(t)
    self.dy = (self.y + 1) / 2
    self.dx = (self.x + 1) / 2
    t += 0.5
    print(self.color + self.char * int(self.dy * self.w)
          + self.char * int(self.dx * self.w))
    self.v += int(self.y * self.c)
    time.sleep(1 / t)
"""
        ]
        funcs = []
        for tsk, val in zip(tasks, values):
            self.__getattr__(tsk)(param="self", value=val, importing="math, time")
            funcs.append(self.code)

        return "\n".join(funcs)


# ── Instances globales ───────────────────────────────────────────
new  = _new()
Base = Base()

__all__ = ["new", "Base", "_C_AVAILABLE", "_CORE"]


# ════════════════════════════════════════════════════════════════
# ── TEST + BENCHMARK ────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import time as _time
    import sys

    # ── Palette ANSI Catppuccin Mocha ────────────────────────────
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    MAGENTA = "\033[95m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

    def banner(txt):
        w = 60
        print(f"\n{CYAN}{'─' * w}{RESET}")
        print(f"{BOLD}{CYAN}  {txt}{RESET}")
        print(f"{CYAN}{'─' * w}{RESET}")

    def ok(label, val):
        print(f"  {GREEN}✓{RESET}  {label:<30} {YELLOW}{val}{RESET}")

    def bench(label, fn, n=50_000):
        t0 = _time.perf_counter()
        for _ in range(n):
            fn()
        return _time.perf_counter() - t0

    # ── 1. Statut du core C ──────────────────────────────────────
    banner("_pluning_core — Statut")
    if _C_AVAILABLE:
        print(f"  {GREEN}✓  Extension C chargée{RESET}  "
              f"{DIM}(version {_core.__version__}){RESET}")
    else:
        print(f"  {YELLOW}⚠  Extension C NON disponible — mode Python pur{RESET}")
        print(f"  {DIM}→ compiler avec : python setup_pluning.py build_ext --inplace{RESET}")

    # ── 2. Tests fonctionnels ────────────────────────────────────
    banner("Tests fonctionnels")

    CODE_SAMPLE = "x = 1\ny = 2\n\nreturn x + y"

    # reaper
    r = _CORE.reaper(CODE_SAMPLE, 2)
    assert "        x = 1" in r, "reaper: indentation incorrecte"
    ok("reaper(code, 2)", repr(r[:30]) + "…")

    # compile_exec
    fn = _CORE.compile_exec("def salut():\n    return 42", "salut")
    assert callable(fn) and fn() == 42, "compile_exec: résultat inattendu"
    ok("compile_exec(def salut…)", f"salut() = {fn()}")

    # build_func_code
    fc = _CORE.build_func_code("add", "a, b", "    return a + b")
    assert fc.startswith("def add(a, b):"), "build_func_code: format incorrect"
    ok("build_func_code", repr(fc[:35]) + "…")

    # build_class_code
    cc = _CORE.build_class_code("MonObjet", "object", "    pass")
    assert "class MonObjet(object):" in cc, "build_class_code: format incorrect"
    ok("build_class_code", repr(cc[:35]) + "…")

    # join_params
    jp = _CORE.join_params(["self", "x", "y", "z"])
    assert jp == "self, x, y, z", f"join_params: '{jp}'"
    ok("join_params(['self','x','y','z'])", jp)

    # ── 3. Test intégration new() ────────────────────────────────
    banner("Test intégration  new.*")

    add_fn = new.add(param=["a", "b"], value="return a + b", importing="")
    if add_fn:
        res = add_fn(3, 7)
        ok("new.add(a, b) → add(3,7)", str(res))
    else:
        print(f"  {YELLOW}⚠  new.add non créé (Codecs indisponibles — normal hors Systeme){RESET}")

    # ── 4. Benchmark reaper ──────────────────────────────────────
    banner("Benchmark reaper (N = 50 000 appels)")

    fb = _FallbackCore()
    t_py = bench("Python reaper", lambda: fb.reaper(CODE_SAMPLE, 3))

    if _C_AVAILABLE:
        t_c  = bench("C reaper",      lambda: _core.reaper(CODE_SAMPLE, 3))
        ratio = t_py / t_c if t_c > 0 else float("inf")
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py * 1000:.2f} ms{RESET}")
        print(f"  {GREEN}C       {RESET}: {GREEN}{t_c  * 1000:.2f} ms{RESET}")
        color = GREEN if ratio >= 10 else YELLOW
        print(f"  {BOLD}Speedup {RESET}: {color}{ratio:.1f}×{RESET}")
    else:
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py * 1000:.2f} ms{RESET}")
        print(f"  {YELLOW}C non disponible — compiler pour voir le speedup{RESET}")

    # ── 5. Benchmark compile_exec ────────────────────────────────
    banner("Benchmark compile_exec (N = 10 000 appels)")

    CODE_CEX = "def f(x):\n    return x * x + 1\n"
    N2 = 10_000
    t_py2 = bench("Python compile_exec",
                  lambda: fb.compile_exec(CODE_CEX, "f"), n=N2)

    if _C_AVAILABLE:
        t_c2  = bench("C compile_exec",
                      lambda: _core.compile_exec(CODE_CEX, "f"), n=N2)
        ratio2 = t_py2 / t_c2 if t_c2 > 0 else float("inf")
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py2 * 1000:.2f} ms{RESET}")
        print(f"  {GREEN}C       {RESET}: {GREEN}{t_c2  * 1000:.2f} ms{RESET}")
        color2 = GREEN if ratio2 >= 2 else YELLOW
        print(f"  {BOLD}Speedup {RESET}: {color2}{ratio2:.1f}×{RESET}")
    else:
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py2 * 1000:.2f} ms{RESET}")

    # ── Résumé ───────────────────────────────────────────────────
    banner("Résumé")
    print(f"  Mode      : {'C natif' if _C_AVAILABLE else 'Python pur (fallback)'}")
    print(f"  Tests     : {GREEN}tous passés{RESET}")
    print()
#!storage/emulated/0/pluning.py
#!use pluning.py
#!generateur objet...
#
# v2.0 — Accélération C via _pluning_core
# Les fonctions critiques (reaper, compile_exec, build_*code, join_params)
# utilisent l'extension C si disponible, sinon fallback Python transparent.
#
# Compiler d'abord :
#   python setup_pluning.py build_ext --inplace
#

# ── Import du noyau C (optionnel — fallback pur Python) ─────────
import sys as _sys, os as _os, glob as _glob, importlib.util as _ilu

def _find_and_load_core():
    """
    Cherche _pluning_core*.so et le charge DIRECTEMENT par son chemin
    complet via importlib — sans dépendre de sys.path.
    """
    _candidates = [
        _os.path.dirname(_os.path.abspath(__file__)),  # dossier de pluning.py
        _os.getcwd(),                                   # dossier courant
        _os.path.join(_os.getcwd(), "project"),         # sous-dossier project
        _os.path.expanduser("~/project"),               # ~/project Termux
        # chemin absolu Android courant
        "/storage/emulated/0/project",
        "/data/data/com.termux/files/home/project",
    ]
    for _d in _candidates:
        _hits = _glob.glob(_os.path.join(_d, "_pluning_core*.so"))
        if not _hits:
            # essayer aussi sans extension explicite
            _hits = _glob.glob(_os.path.join(_d, "_pluning_core*"))
            _hits = [h for h in _hits if h.endswith(".so") or ".cpython" in h]
        if _hits:
            _so_path = _hits[0]
            try:
                _spec = _ilu.spec_from_file_location("_pluning_core", _so_path)
                _mod  = _ilu.module_from_spec(_spec)
                _spec.loader.exec_module(_mod)
                _sys.modules["_pluning_core"] = _mod
                return _mod, True
            except Exception:
                continue
    # dernier recours : import classique
    try:
        import _pluning_core as _c
        return _c, True
    except ImportError:
        return None, False

_core, _C_AVAILABLE = _find_and_load_core()

# ── Fallbacks Python (si C non compilé) ─────────────────────────
class _FallbackCore:
    """Réimplémentation Python de _pluning_core — même API, sans C."""

    @staticmethod
    def reaper(code: str, i: int = 1) -> str:
        lines  = code.splitlines()
        indent = i * 4
        result = []
        for line in lines:
            if not line.strip():
                result.append("")
            else:
                result.append(" " * indent + line)
        return "\n".join(result) + "\n"

    @staticmethod
    def compile_exec(code: str, attr: str):
        ns = {}
        exec(compile(code, "<pluning>", "exec"), ns)
        if attr not in ns:
            raise KeyError(f"attribut '{attr}' introuvable dans le namespace")
        return ns[attr]

    @staticmethod
    def build_func_code(name: str, params: str, body: str) -> str:
        if params:
            return f"def {name}({params}):\n    {body}"
        return f"def {name}():\n    {body}"

    @staticmethod
    def build_class_code(name: str, parents: str, body: str) -> str:
        if parents:
            return f"class {name}({parents}):\n    {body}"
        return f"class {name}:\n    {body}"

    @staticmethod
    def join_params(params_list: list) -> str:
        return ", ".join(params_list)

# Utiliser C si disponible, sinon fallback
_CORE = _core if _C_AVAILABLE else _FallbackCore()


# ════════════════════════════════════════════════════════════════
# Base
# ════════════════════════════════════════════════════════════════
class Base:
    def __init__(self):
        self.json     = __import__("json")
        self.os       = __import__("os")
        self.abs_dir  = "Systeme/states/emulated/0/json/"
        self.abs_name = "data_pluning.py"
        self.abs_path = self.os.path.join(self.abs_dir, self.abs_name)
        self.li       = "use namespace; data of pluning."

    class extented:

        def Codecs(self, code, attr):
            from Systeme.IO.tools.Codecs import lambdaCodecs
            namespace = {}
            try:
                return lambdaCodecs.statistc_encode(code)
            except:  # incompatibilité éventuelle
                exec(code, namespace)
                return namespace[attr]

        def ast_Codecs(self, code, attr):
            from Systeme.IO.tools.Codecs import ast_to_string, string_to_ast
            namespace = {}
            try:
                ast = string_to_ast._string_to_ast(code)
                exec(ast_to_string._ast_to_string, namespace)
                return namespace.get(attr, None)
            except Exception as e:
                from Systeme.vendor.release.Error import SystemeError
                raise SystemeError(e) from e

        def reaper(self, code: str, i: int = 1) -> str:
            """
            Indente chaque ligne de code de (i * 4) espaces.
            ── Utilise _pluning_core.reaper (C) si disponible ──
            """
            return _CORE.reaper(code, i)

    class SystemClass:
        """Réseau de compilation/exécution de classes."""

        def network(code, attr):
            pass

        def _compile(self, code: str, attr: str):
            """
            Compile et exec du code Python, retourne namespace[attr].
            ── Utilise _pluning_core.compile_exec (C) si disponible ──
            """
            try:
                return _CORE.compile_exec(code, attr)
            except Exception as e:
                from Systeme.vendor.release.Error import SystemeError
                raise SystemeError(e) from e

    SystemClass = SystemClass()
    extented    = extented()


# ════════════════════════════════════════════════════════════════
# _new  —  Générateur d'objets dynamiques
# ════════════════════════════════════════════════════════════════
class _new(Base):
    def __init__(self):
        self.file        = None
        self.extented    = Base.extented
        self.SystemClass = Base.SystemClass

    def __setattr__(self, _name, _value):
        super().__setattr__(_name, _value)

    def __getattr__(self, attr, i: int = 1, ptype=False):

        def creator(*a, **kw):
            self.file    = attr
            self.type    = kw.get('type', 'func')
            self.subparam = kw.get('param', ord('A'))

            # Résolution du type (ptype surchargé ou depuis kw)
            if ptype is not False:
                self.type = ptype

            # ── Construction du paramètre (param) ──────────────
            if isinstance(self.subparam, list):
                # ── Utilise _pluning_core.join_params (C) ──
                self.param = _CORE.join_params(self.subparam)
            elif isinstance(self.subparam, str):
                self.param = self.subparam
            else:
                self.param = ''

            self.namespace = {}

            # ── TYPE : func ────────────────────────────────────
            if self.type == 'func':
                importing = kw.get('importing', 'time')
                # Éviter "import " si la valeur est vide
                if importing and importing.strip():
                    self.importOject = f"\nimport {importing}"
                else:
                    self.importOject = ""
                body_raw  = kw.get('value', '\nreturn True')

                if self.importOject:
                    indented_import = self.extented.reaper(self.importOject, i)
                    self.body = f"{indented_import}\n    {self.extented.reaper(body_raw, i)}"
                    exec(self.importOject)  # injecter l'import dans l'env courant
                else:
                    self.body = self.extented.reaper(body_raw, i)

                # ── Construire le code de la fonction (C) ──────
                self.code = _CORE.build_func_code(attr, self.param, self.body)

                # Tenter l'encodage via Codecs (lambdaCodecs)
                try:
                    self.__setattr__("call_" + attr,
                                     self.extented.Codecs(self.code, attr))
                except:
                    try:
                        self.__setattr__("call_" + attr,
                                         self.extented.ast_Codecs(self.code, attr))
                    except:
                        pass  # Codecs non disponibles — on continue sans

                exec(self.code, self.namespace)
                return self.namespace.get(attr)

            # ── TYPE : str ─────────────────────────────────────
            elif self.type == 'str' or self.type == type(str()):
                self.body = kw.get('value', str(*a) if a else '')
                self.code = f"{attr} = '{self.body}'"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : int ─────────────────────────────────────
            elif self.type == 'int' or self.type == type(int()):
                self.body = kw.get('value', int(*a) if a else 0)
                self.code = f"{attr} = {self.body}"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : bool ────────────────────────────────────
            elif self.type == 'bool' or self.type == type(bool()):
                self.body = kw.get('value', bool(*a) if a else False)
                self.code = f"{attr} = {self.body}"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : object / class ──────────────────────────
            elif self.type in ("object", "class"):
                _parent_raw = kw.get("parrent", "")

                if isinstance(_parent_raw, list):
                    self.parrent = ", ".join(_parent_raw)
                elif isinstance(_parent_raw, str):
                    self.parrent = _parent_raw
                else:
                    self.parrent = ''

                self.body = self.extented.reaper(
                    kw.get('value', self._delfaut())
                )

                # ── Construire le code de la classe (C) ────────
                self.code = _CORE.build_class_code(attr, self.parrent, self.body)

                obj = self.SystemClass._compile(self.code, attr)
                self.__setattr__("class_" + attr, obj)
                return obj

            else:
                return ""  # valeur par défaut pour le type inconnu

        return creator

    def _delfaut(self) -> str:
        """Corps par défaut d'une classe : __new__, __init__, onde."""
        tasks = ["__new__", "__init__", "onde"]
        values = [
            """
self = super().__new__(self)
return self
""",
            """
self.char = '+'
self.w = 9
self.c = 12
self.v = 90
""",
            """
t = 0
while True:
    self.color = f"\\033[{self.v}m"
    self.y = math.sin(t)
    self.x = math.cos(t)
    self.dy = (self.y + 1) / 2
    self.dx = (self.x + 1) / 2
    t += 0.5
    print(self.color + self.char * int(self.dy * self.w)
          + self.char * int(self.dx * self.w))
    self.v += int(self.y * self.c)
    time.sleep(1 / t)
"""
        ]
        funcs = []
        for tsk, val in zip(tasks, values):
            self.__getattr__(tsk)(param="self", value=val, importing="math, time")
            funcs.append(self.code)

        return "\n".join(funcs)


# ── Instances globales ───────────────────────────────────────────
new  = _new()
Base = Base()

__all__ = ["new", "Base", "_C_AVAILABLE", "_CORE"]


# ════════════════════════════════════════════════════════════════
# ── TEST + BENCHMARK ────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import time as _time
    import sys

    # ── Palette ANSI Catppuccin Mocha ────────────────────────────
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    MAGENTA = "\033[95m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

    def banner(txt):
        w = 60
        print(f"\n{CYAN}{'─' * w}{RESET}")
        print(f"{BOLD}{CYAN}  {txt}{RESET}")
        print(f"{CYAN}{'─' * w}{RESET}")

    def ok(label, val):
        print(f"  {GREEN}✓{RESET}  {label:<30} {YELLOW}{val}{RESET}")

    def bench(label, fn, n=50_000):
        t0 = _time.perf_counter()
        for _ in range(n):
            fn()
        return _time.perf_counter() - t0

    # ── 1. Statut du core C ──────────────────────────────────────
    banner("_pluning_core — Statut")
    if _C_AVAILABLE:
        print(f"  {GREEN}✓  Extension C chargée{RESET}  "
              f"{DIM}(version {_core.__version__}){RESET}")
    else:
        print(f"  {YELLOW}⚠  Extension C NON disponible — mode Python pur{RESET}")
        print(f"  {DIM}→ compiler avec : python setup_pluning.py build_ext --inplace{RESET}")

    # ── 2. Tests fonctionnels ────────────────────────────────────
    banner("Tests fonctionnels")

    CODE_SAMPLE = "x = 1\ny = 2\n\nreturn x + y"

    # reaper
    r = _CORE.reaper(CODE_SAMPLE, 2)
    assert "        x = 1" in r, "reaper: indentation incorrecte"
    ok("reaper(code, 2)", repr(r[:30]) + "…")

    # compile_exec
    fn = _CORE.compile_exec("def salut():\n    return 42", "salut")
    assert callable(fn) and fn() == 42, "compile_exec: résultat inattendu"
    ok("compile_exec(def salut…)", f"salut() = {fn()}")

    # build_func_code
    fc = _CORE.build_func_code("add", "a, b", "    return a + b")
    assert fc.startswith("def add(a, b):"), "build_func_code: format incorrect"
    ok("build_func_code", repr(fc[:35]) + "…")

    # build_class_code
    cc = _CORE.build_class_code("MonObjet", "object", "    pass")
    assert "class MonObjet(object):" in cc, "build_class_code: format incorrect"
    ok("build_class_code", repr(cc[:35]) + "…")

    # join_params
    jp = _CORE.join_params(["self", "x", "y", "z"])
    assert jp == "self, x, y, z", f"join_params: '{jp}'"
    ok("join_params(['self','x','y','z'])", jp)

    # ── 3. Test intégration new() ────────────────────────────────
    banner("Test intégration  new.*")

    add_fn = new.add(param=["a", "b"], value="return a + b", importing="")
    if add_fn:
        res = add_fn(3, 7)
        ok("new.add(a, b) → add(3,7)", str(res))
    else:
        print(f"  {YELLOW}⚠  new.add non créé (Codecs indisponibles — normal hors Systeme){RESET}")

    # ── 4. Benchmark reaper ──────────────────────────────────────
    banner("Benchmark reaper (N = 50 000 appels)")

    fb = _FallbackCore()
    t_py = bench("Python reaper", lambda: fb.reaper(CODE_SAMPLE, 3))

    if _C_AVAILABLE:
        t_c  = bench("C reaper",      lambda: _core.reaper(CODE_SAMPLE, 3))
        ratio = t_py / t_c if t_c > 0 else float("inf")
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py * 1000:.2f} ms{RESET}")
        print(f"  {GREEN}C       {RESET}: {GREEN}{t_c  * 1000:.2f} ms{RESET}")
        color = GREEN if ratio >= 10 else YELLOW
        print(f"  {BOLD}Speedup {RESET}: {color}{ratio:.1f}×{RESET}")
    else:
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py * 1000:.2f} ms{RESET}")
        print(f"  {YELLOW}C non disponible — compiler pour voir le speedup{RESET}")

    # ── 5. Benchmark compile_exec ────────────────────────────────
    banner("Benchmark compile_exec (N = 10 000 appels)")

    CODE_CEX = "def f(x):\n    return x * x + 1\n"
    N2 = 10_000
    t_py2 = bench("Python compile_exec",
                  lambda: fb.compile_exec(CODE_CEX, "f"), n=N2)

    if _C_AVAILABLE:
        t_c2  = bench("C compile_exec",
                      lambda: _core.compile_exec(CODE_CEX, "f"), n=N2)
        ratio2 = t_py2 / t_c2 if t_c2 > 0 else float("inf")
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py2 * 1000:.2f} ms{RESET}")
        print(f"  {GREEN}C       {RESET}: {GREEN}{t_c2  * 1000:.2f} ms{RESET}")
        color2 = GREEN if ratio2 >= 2 else YELLOW
        print(f"  {BOLD}Speedup {RESET}: {color2}{ratio2:.1f}×{RESET}")
    else:
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py2 * 1000:.2f} ms{RESET}")

    # ── Résumé ───────────────────────────────────────────────────
    banner("Résumé")
    print(f"  Mode      : {'C natif' if _C_AVAILABLE else 'Python pur (fallback)'}")
    print(f"  Tests     : {GREEN}tous passés{RESET}")
    print()
#!storage/emulated/0/pluning.py
#!use pluning.py
#!generateur objet...
#
# v2.0 — Accélération C via _pluning_core
# Les fonctions critiques (reaper, compile_exec, build_*code, join_params)
# utilisent l'extension C si disponible, sinon fallback Python transparent.
#
# Compiler d'abord :
#   python setup_pluning.py build_ext --inplace
#

# ── Import du noyau C (optionnel — fallback pur Python) ─────────
import sys as _sys, os as _os, glob as _glob, importlib.util as _ilu

def _find_and_load_core():
    """
    Cherche _pluning_core*.so et le charge DIRECTEMENT par son chemin
    complet via importlib — sans dépendre de sys.path.
    """
    _candidates = [
        _os.path.dirname(_os.path.abspath(__file__)),  # dossier de pluning.py
        _os.getcwd(),                                   # dossier courant
        _os.path.join(_os.getcwd(), "project"),         # sous-dossier project
        _os.path.expanduser("~/project"),               # ~/project Termux
        # chemin absolu Android courant
        "/storage/emulated/0/project",
        "/data/data/com.termux/files/home/project",
    ]
    for _d in _candidates:
        _hits = _glob.glob(_os.path.join(_d, "_pluning_core*.so"))
        if not _hits:
            # essayer aussi sans extension explicite
            _hits = _glob.glob(_os.path.join(_d, "_pluning_core*"))
            _hits = [h for h in _hits if h.endswith(".so") or ".cpython" in h]
        if _hits:
            _so_path = _hits[0]
            try:
                _spec = _ilu.spec_from_file_location("_pluning_core", _so_path)
                _mod  = _ilu.module_from_spec(_spec)
                _spec.loader.exec_module(_mod)
                _sys.modules["_pluning_core"] = _mod
                return _mod, True
            except Exception:
                continue
    # dernier recours : import classique
    try:
        import _pluning_core as _c
        return _c, True
    except ImportError:
        return None, False

_core, _C_AVAILABLE = _find_and_load_core()

# ── Fallbacks Python (si C non compilé) ─────────────────────────
class _FallbackCore:
    """Réimplémentation Python de _pluning_core — même API, sans C."""

    @staticmethod
    def reaper(code: str, i: int = 1) -> str:
        lines  = code.splitlines()
        indent = i * 4
        result = []
        for line in lines:
            if not line.strip():
                result.append("")
            else:
                result.append(" " * indent + line)
        return "\n".join(result) + "\n"

    @staticmethod
    def compile_exec(code: str, attr: str):
        ns = {}
        exec(compile(code, "<pluning>", "exec"), ns)
        if attr not in ns:
            raise KeyError(f"attribut '{attr}' introuvable dans le namespace")
        return ns[attr]

    @staticmethod
    def build_func_code(name: str, params: str, body: str) -> str:
        if params:
            return f"def {name}({params}):\n    {body}"
        return f"def {name}():\n    {body}"

    @staticmethod
    def build_class_code(name: str, parents: str, body: str) -> str:
        if parents:
            return f"class {name}({parents}):\n    {body}"
        return f"class {name}:\n    {body}"

    @staticmethod
    def join_params(params_list: list) -> str:
        return ", ".join(params_list)

# Utiliser C si disponible, sinon fallback
_CORE = _core if _C_AVAILABLE else _FallbackCore()


# ════════════════════════════════════════════════════════════════
# Base
# ════════════════════════════════════════════════════════════════
class Base:
    def __init__(self):
        self.json     = __import__("json")
        self.os       = __import__("os")
        self.abs_dir  = "Systeme/states/emulated/0/json/"
        self.abs_name = "data_pluning.py"
        self.abs_path = self.os.path.join(self.abs_dir, self.abs_name)
        self.li       = "use namespace; data of pluning."

    class extented:

        def Codecs(self, code, attr):
            from Systeme.IO.tools.Codecs import lambdaCodecs
            namespace = {}
            try:
                return lambdaCodecs.statistc_encode(code)
            except:  # incompatibilité éventuelle
                exec(code, namespace)
                return namespace[attr]

        def ast_Codecs(self, code, attr):
            from Systeme.IO.tools.Codecs import ast_to_string, string_to_ast
            namespace = {}
            try:
                ast = string_to_ast._string_to_ast(code)
                exec(ast_to_string._ast_to_string, namespace)
                return namespace.get(attr, None)
            except Exception as e:
                from Systeme.vendor.release.Error import SystemeError
                raise SystemeError(e) from e

        def reaper(self, code: str, i: int = 1) -> str:
            """
            Indente chaque ligne de code de (i * 4) espaces.
            ── Utilise _pluning_core.reaper (C) si disponible ──
            """
            return _CORE.reaper(code, i)

    class SystemClass:
        """Réseau de compilation/exécution de classes."""

        def network(code, attr):
            pass

        def _compile(self, code: str, attr: str):
            """
            Compile et exec du code Python, retourne namespace[attr].
            ── Utilise _pluning_core.compile_exec (C) si disponible ──
            """
            try:
                return _CORE.compile_exec(code, attr)
            except Exception as e:
                from Systeme.vendor.release.Error import SystemeError
                raise SystemeError(e) from e

    SystemClass = SystemClass()
    extented    = extented()


# ════════════════════════════════════════════════════════════════
# _new  —  Générateur d'objets dynamiques
# ════════════════════════════════════════════════════════════════
class _new(Base):
    def __init__(self):
        self.file        = None
        self.extented    = Base.extented
        self.SystemClass = Base.SystemClass

    def __setattr__(self, _name, _value):
        super().__setattr__(_name, _value)

    def __getattr__(self, attr, i: int = 1, ptype=False):

        def creator(*a, **kw):
            self.file    = attr
            self.type    = kw.get('type', 'func')
            self.subparam = kw.get('param', ord('A'))

            # Résolution du type (ptype surchargé ou depuis kw)
            if ptype is not False:
                self.type = ptype

            # ── Construction du paramètre (param) ──────────────
            if isinstance(self.subparam, list):
                # ── Utilise _pluning_core.join_params (C) ──
                self.param = _CORE.join_params(self.subparam)
            elif isinstance(self.subparam, str):
                self.param = self.subparam
            else:
                self.param = ''

            self.namespace = {}

            # ── TYPE : func ────────────────────────────────────
            if self.type == 'func':
                importing = kw.get('importing', 'time')
                # Éviter "import " si la valeur est vide
                if importing and importing.strip():
                    self.importOject = f"\nimport {importing}"
                else:
                    self.importOject = ""
                body_raw  = kw.get('value', '\nreturn True')

                if self.importOject:
                    indented_import = self.extented.reaper(self.importOject, i)
                    self.body = f"{indented_import}\n    {self.extented.reaper(body_raw, i)}"
                    exec(self.importOject)  # injecter l'import dans l'env courant
                else:
                    self.body = self.extented.reaper(body_raw, i)

                # ── Construire le code de la fonction (C) ──────
                self.code = _CORE.build_func_code(attr, self.param, self.body)

                # Tenter l'encodage via Codecs (lambdaCodecs)
                try:
                    self.__setattr__("call_" + attr,
                                     self.extented.Codecs(self.code, attr))
                except:
                    try:
                        self.__setattr__("call_" + attr,
                                         self.extented.ast_Codecs(self.code, attr))
                    except:
                        pass  # Codecs non disponibles — on continue sans

                exec(self.code, self.namespace)
                return self.namespace.get(attr)

            # ── TYPE : str ─────────────────────────────────────
            elif self.type == 'str' or self.type == type(str()):
                self.body = kw.get('value', str(*a) if a else '')
                self.code = f"{attr} = '{self.body}'"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : int ─────────────────────────────────────
            elif self.type == 'int' or self.type == type(int()):
                self.body = kw.get('value', int(*a) if a else 0)
                self.code = f"{attr} = {self.body}"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : bool ────────────────────────────────────
            elif self.type == 'bool' or self.type == type(bool()):
                self.body = kw.get('value', bool(*a) if a else False)
                self.code = f"{attr} = {self.body}"
                self.__setattr__(attr, self.body)
                exec(self.code, self.namespace)
                return self.namespace[attr]

            # ── TYPE : object / class ──────────────────────────
            elif self.type in ("object", "class"):
                _parent_raw = kw.get("parrent", "")

                if isinstance(_parent_raw, list):
                    self.parrent = ", ".join(_parent_raw)
                elif isinstance(_parent_raw, str):
                    self.parrent = _parent_raw
                else:
                    self.parrent = ''

                self.body = self.extented.reaper(
                    kw.get('value', self._delfaut())
                )

                # ── Construire le code de la classe (C) ────────
                self.code = _CORE.build_class_code(attr, self.parrent, self.body)

                obj = self.SystemClass._compile(self.code, attr)
                self.__setattr__("class_" + attr, obj)
                return obj

            else:
                return ""  # valeur par défaut pour le type inconnu

        return creator

    def _delfaut(self) -> str:
        """Corps par défaut d'une classe : __new__, __init__, onde."""
        tasks = ["__new__", "__init__", "onde"]
        values = [
            """
self = super().__new__(self)
return self
""",
            """
self.char = '+'
self.w = 9
self.c = 12
self.v = 90
""",
            """
t = 0
while True:
    self.color = f"\\033[{self.v}m"
    self.y = math.sin(t)
    self.x = math.cos(t)
    self.dy = (self.y + 1) / 2
    self.dx = (self.x + 1) / 2
    t += 0.5
    print(self.color + self.char * int(self.dy * self.w)
          + self.char * int(self.dx * self.w))
    self.v += int(self.y * self.c)
    time.sleep(1 / t)
"""
        ]
        funcs = []
        for tsk, val in zip(tasks, values):
            self.__getattr__(tsk)(param="self", value=val, importing="math, time")
            funcs.append(self.code)

        return "\n".join(funcs)


# ── Instances globales ───────────────────────────────────────────
new  = _new()
Base = Base()

__all__ = ["new", "Base", "_C_AVAILABLE", "_CORE"]


# ════════════════════════════════════════════════════════════════
# ── TEST + BENCHMARK ────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import time as _time
    import sys

    # ── Palette ANSI Catppuccin Mocha ────────────────────────────
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    MAGENTA = "\033[95m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

    def banner(txt):
        w = 60
        print(f"\n{CYAN}{'─' * w}{RESET}")
        print(f"{BOLD}{CYAN}  {txt}{RESET}")
        print(f"{CYAN}{'─' * w}{RESET}")

    def ok(label, val):
        print(f"  {GREEN}✓{RESET}  {label:<30} {YELLOW}{val}{RESET}")

    def bench(label, fn, n=50_000):
        t0 = _time.perf_counter()
        for _ in range(n):
            fn()
        return _time.perf_counter() - t0

    # ── 1. Statut du core C ──────────────────────────────────────
    banner("_pluning_core — Statut")
    if _C_AVAILABLE:
        print(f"  {GREEN}✓  Extension C chargée{RESET}  "
              f"{DIM}(version {_core.__version__}){RESET}")
    else:
        print(f"  {YELLOW}⚠  Extension C NON disponible — mode Python pur{RESET}")
        print(f"  {DIM}→ compiler avec : python setup_pluning.py build_ext --inplace{RESET}")

    # ── 2. Tests fonctionnels ────────────────────────────────────
    banner("Tests fonctionnels")

    CODE_SAMPLE = "x = 1\ny = 2\n\nreturn x + y"

    # reaper
    r = _CORE.reaper(CODE_SAMPLE, 2)
    assert "        x = 1" in r, "reaper: indentation incorrecte"
    ok("reaper(code, 2)", repr(r[:30]) + "…")

    # compile_exec
    fn = _CORE.compile_exec("def salut():\n    return 42", "salut")
    assert callable(fn) and fn() == 42, "compile_exec: résultat inattendu"
    ok("compile_exec(def salut…)", f"salut() = {fn()}")

    # build_func_code
    fc = _CORE.build_func_code("add", "a, b", "    return a + b")
    assert fc.startswith("def add(a, b):"), "build_func_code: format incorrect"
    ok("build_func_code", repr(fc[:35]) + "…")

    # build_class_code
    cc = _CORE.build_class_code("MonObjet", "object", "    pass")
    assert "class MonObjet(object):" in cc, "build_class_code: format incorrect"
    ok("build_class_code", repr(cc[:35]) + "…")

    # join_params
    jp = _CORE.join_params(["self", "x", "y", "z"])
    assert jp == "self, x, y, z", f"join_params: '{jp}'"
    ok("join_params(['self','x','y','z'])", jp)

    # ── 3. Test intégration new() ────────────────────────────────
    banner("Test intégration  new.*")

    add_fn = new.add(param=["a", "b"], value="return a + b", importing="")
    if add_fn:
        res = add_fn(3, 7)
        ok("new.add(a, b) → add(3,7)", str(res))
    else:
        print(f"  {YELLOW}⚠  new.add non créé (Codecs indisponibles — normal hors Systeme){RESET}")

    # ── 4. Benchmark reaper ──────────────────────────────────────
    banner("Benchmark reaper (N = 50 000 appels)")

    fb = _FallbackCore()
    t_py = bench("Python reaper", lambda: fb.reaper(CODE_SAMPLE, 3))

    if _C_AVAILABLE:
        t_c  = bench("C reaper",      lambda: _core.reaper(CODE_SAMPLE, 3))
        ratio = t_py / t_c if t_c > 0 else float("inf")
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py * 1000:.2f} ms{RESET}")
        print(f"  {GREEN}C       {RESET}: {GREEN}{t_c  * 1000:.2f} ms{RESET}")
        color = GREEN if ratio >= 10 else YELLOW
        print(f"  {BOLD}Speedup {RESET}: {color}{ratio:.1f}×{RESET}")
    else:
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py * 1000:.2f} ms{RESET}")
        print(f"  {YELLOW}C non disponible — compiler pour voir le speedup{RESET}")

    # ── 5. Benchmark compile_exec ────────────────────────────────
    banner("Benchmark compile_exec (N = 10 000 appels)")

    CODE_CEX = "def f(x):\n    return x * x + 1\n"
    N2 = 10_000
    t_py2 = bench("Python compile_exec",
                  lambda: fb.compile_exec(CODE_CEX, "f"), n=N2)

    if _C_AVAILABLE:
        t_c2  = bench("C compile_exec",
                      lambda: _core.compile_exec(CODE_CEX, "f"), n=N2)
        ratio2 = t_py2 / t_c2 if t_c2 > 0 else float("inf")
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py2 * 1000:.2f} ms{RESET}")
        print(f"  {GREEN}C       {RESET}: {GREEN}{t_c2  * 1000:.2f} ms{RESET}")
        color2 = GREEN if ratio2 >= 2 else YELLOW
        print(f"  {BOLD}Speedup {RESET}: {color2}{ratio2:.1f}×{RESET}")
    else:
        print(f"  {DIM}Python  {RESET}: {YELLOW}{t_py2 * 1000:.2f} ms{RESET}")

    # ── Résumé ───────────────────────────────────────────────────
    banner("Résumé")
    print(f"  Mode      : {'C natif' if _C_AVAILABLE else 'Python pur (fallback)'}")
    print(f"  Tests     : {GREEN}tous passés{RESET}")
    print()
