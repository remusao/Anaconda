

(* ----- *)
(*  MOD  *)
(* ----- *)

type _ modl =
    | EmptyModule
    | Module        : 'a stmt * 'b modl -> ('a stmt * 'b modl) modl
    | Interactive   : 'a stmt * 'b modl -> ('a stmt * 'b modl) modl
    | Expression    : 'a expr -> ('a expr) modl


(* ---- *)
(* STMT *)
(* ---- *)

and _ stmt =
    | EmptyStmt
    | FunctionDef
        of identifier           (* name *)
        *  arguments            (* arguments *)
        *  stmt list            (* body *)
        *  expr list            (* decorator_list *)
        *  expr                 (* ? return statement *)
    | ClassDef
        of identifier           (* name *)
        *  expr list            (* bases *)
        *  keyword list         (* keywords *)
        *  expr                 (* ? starargs *)
        *  expr                 (* ? kwargs *)
        *  stmt list            (* body *)
        *  expr list            (* decorator_list *)
    | Return of expr            (* ? value *)
    | Delete of expr list       (* targets *)
    | Assign
        of expr list            (* targets *)
        *  expr                 (* value *)
    | AugAssign
        of expr                 (* target *)
        *  operator             (* op *)
        *  expr                 (* value *)

    (* -- use 'orelse' because else is a keyword in target languages *)

    | For
        of expr                 (* target *)
        *  expr                 (* iter *)
        * stmt list             (* body *)
        * stmt list             (* orelse *)
    | While
        of expr                 (* test *)
        *  stmt list            (* body *)
        *  stmt list            (* orelse *)
    | If
        of expr                 (* test *)
        *  stmt list            (* body *)
        *  stmt list            (* orelse *)
    | With
        of withitem list        (* items *)
        *  stmt list            (* body *)

    | Raise
        of expr                 (* ? exc *)
        *  expr                 (* ? cause *)
    | Try
        of stmt list            (* body *)
        *  excepthandler list   (* handlers *)
        *  stmt list            (* orelse *)
        *  stmt list            (* finalbody *)
    | Assert
        of expr                 (* test *)
        * expr                  (* ?msg *)

    | Import of alias list      (* names *)
    | ImportFrom
        of identifier           (* ? module *)
        * alias list            (* names *)
        * int                   (* ? level *)

    | Global of identifier list (* names *)
    | Nonlocal of identifier list (* names *)
    | Expr of expr              (* value *)
    | Pass
    | Break
    | Continue


(* ---- *)
(* EXPR *)
(* ---- *)

and _ expr =
      BoolOp
        of boolop       (* op *)
        *  expr list    (* values *)
    | BinOp
        of expr         (* left *)
        *  operator     (* op *)
        *  expr         (* right *)
    | UnaryOp
        of unaryop      (* op *)
        *  expr         (* operand *)
    | Lambda
        of arguments    (* args *)
        *  expr         (* body *)
    | IfExp
        of expr         (* test *)
        *  expr         (* body *)
        *  expr         (* orelse *)
    | Dict
        of expr list    (* keys *)
        *  expr list    (* values *)
    | Set of expr list  (* elts *)
    | ListComp
        of expr         (* elt *)
        *  comprehension list   (* generators *)
    | SetComp
        of expr         (* elt *)
        *  comprehension list  (* generators *)
    | DictComp
        of expr         (* key *)
        *  expr         (* value *)
        *  comprehension list (* generators *)
    | GeneratorExp
        of expr         (* elt *)
        *  comprehension list   (* generators *)


(* -- the grammar constrains where yield expressions can occur *)

    | Yield of expr     (* ? value *)
    | YieldFrom of expr (* ? value *)


(* -- need sequences for compare to distinguish between *)
(* -- x < 4 < 3 and (x < 4) < 3 *)

    | Compare
        of expr         (* left *)
        *  cmpop list   (* ops *)
        *  expr list    (* comparators *)
    | Call
        of expr         (* func *)
        *  expr list    (* args *)
        *  keyword list (* keywords *)
        *  expr         (* ? starargs *)
        *  expr         (* ? kwargs *)
    | Num of num        (* (object n) -- a number as a PyObject. *)
    | Str of string     (* s -- need to specify raw, unicode, etc? *)
    | Bytes of int list (* bytes s -- Immutable sequence of integers 0 <= x <= 256 *)
    | Ellipsis

    (* -- other literals? bools? *)
    (* -- the following expression can appear in assignment context *)

    | Attribute
        of expr         (* value *)
        *  identifier   (* attr *)
        *  expr_context (* ctx *)
    | Subscript
        of expr         (* value *)
        *  slice        (* slice *)
        *  expr_context (* ctx *)
    | Starred
        of expr         (* value *)
        *  expr_context (* ctx *)
    | Name
        of identifier   (* id *)
        *  expr_context (* ctx *)
    | List
        of expr list    (* elts *)
        *  expr_context (* ctx *)
    | Tuple
        of expr list    (* elts *)
        *  expr_context (* ctx *)

    (* -- col_offset is the byte offset in the utf8 string the parser uses  *)
    (*    attributes (int lineno, int col_offset)                           *)


and expr_context =
      Load
    | Store
    | Del
    | AugLoad
    | AugStore
    | Param


and slice =
      Slice
        of expr         (* ? lower *)
        *  expr         (* ? upper *)
        *  expr         (* ? step *)
    | ExtSlice of slice list (* dims *)
    | Index of expr     (* value *)


and boolop =
      And
    | Or


and operator =
      Add
    | Sub
    | Mult
    | Div
    | Mod
    | Pow
    | LShift
    | RShift
    | BitOr
    | BitXor
    | BitAnd
    | FloorDiv


and unaryop =
      Invert
    | Not
    | UAdd
    | USub


and cmpop =
      Eq
    | NotEq
    | Lt
    | LtE
    | Gt
    | GtE
    | Is
    | IsNot
    | In
    | NotIn


(* Primitive types *)


and identifier = Identifier of string

and num =
    | Int of int
    | Float of float

and arguments =
    Arguments
        of arg list     (* args *)
        *  identifier   (* ? vararg *)
        *  expr         (* ? varargannotation *)
        *  arg list     (* kwonlyargs *)
        *  identifier   (* ? kwarg *)
        *  expr         (* ? kwargannotation *)
        *  expr list    (* defaults *)
        *  expr list    (* kw_defaults *)

and exceptHandler =
    ExceptHandler
        of expr         (* ? type *)
        *  identifier   (* ? name *)
        *  stmt list    (* body *)

and attributes =
    Attributes
        of int          (* lineno *)
        *  int          (* col_offset *)

and comprehension =
    Comprehension
        of expr         (* target *)
        *  expr         (* iter *)
        *  expr list    (* ifs *)

and arg =
    Arg
        of identifier   (* arg *)
        *  expr         (* ? annotation *)

(* -- keyword arguments supplied to call *)

and keyword =
    Keyword
        of identifier   (* arg *)
        *  expr         (* value *)

(* -- import name with optional 'as' alias. *)

and alias =
    Alias
        of identifier   (* name *)
        *  identifier   (* ? asname *)

and withitem =
    Withitem
        of expr         (* context_expr *)
        *  expr         (* ? optional_vars *)
