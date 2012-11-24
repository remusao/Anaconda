{
    (* Header *)
    open Lexer_state
    open Lexing
    open Parser

    let curr_pos lexbuf = lexbuf.lex_start_p
    let count_lines s =
        let n = ref 0 in
        String.iter (fun c -> if c = '\n' then incr n)
        s;
    !n

  let unescaped s =
    let buf = Buffer.create (String.length s) in
    let escape = ref false in
    let unescapechar c =
      if !escape then begin
        match c with
        | '\r' -> ()
        | '\n' -> escape := false
        | _ -> begin
            escape := false;
            (* TODO http://docs.python.org/reference/lexical_analysis.html#string-literals *)
            Buffer.add_char
              buf
              (match c with
               | '\\' -> '\\'
               | '\'' -> '\''
               | '"' -> '"'
               | 'a' -> Char.chr 7
               | 'b' -> '\b'
               | 'f' -> Char.chr 12
               | 'n' -> '\n'
               | 'r' -> '\r'
               | 't' -> '\t'
               | 'v' -> Char.chr 11
               | _ -> (Buffer.add_char buf '\\'; c))
          end
      end else if c = '\\' then
        escape := true
      else
        Buffer.add_char buf c
    in
      String.iter unescapechar s;
      Buffer.contents buf

    (* Keyword Hash table *)

    let kwd =
        [|("and",       (fun x -> AND(x)));
          ("as",        (fun x -> AS(x)));
          ("assert",    (fun x -> ASSERT(x)));
          ("break",     (fun x -> BREAK(x)));
          ("class",     (fun x -> CLASS(x)));
          ("continue",  (fun x -> CONTINUE(x)));
          ("def",       (fun x -> DEF(x)));
          ("del",       (fun x -> DEL(x)));
          ("elif",      (fun x -> ELIF(x)));
          ("else",      (fun x -> ELSE(x)));
          ("except",    (fun x -> EXCEPT(x)));
          ("exec",      (fun x -> EXEC(x)));
          ("finally",   (fun x -> FINALLY(x)));
          ("for",       (fun x -> FOR(x)));
          ("from",      (fun x -> FROM(x)));
          ("global",    (fun x -> GLOBAL(x)));
          ("if",        (fun x -> IF(x)));
          ("import",    (fun x -> IMPORT(x)));
          ("in",        (fun x -> IN(x)));
          ("is",        (fun x -> IS(x)));
          ("lambda",    (fun x -> LAMBDA(x)));
          ("not",       (fun x -> NOT(x)));
          ("or",        (fun x -> OR(x)));
          ("pass",      (fun x -> PASS(x)));
          ("print",     (fun x -> PRINT(x)));
          ("raise",     (fun x -> RAISE(x)));
          ("return",    (fun x -> RETURN(x)));
          ("try",       (fun x -> TRY(x)));
          ("while",     (fun x -> WHILE(x)));
          ("with",      (fun x -> WITH(x)));
          ("yield",     (fun x -> YIELD(x)));
        |]
    let keywords = Hashtbl.create (Array.length kwd)
    let _ = Array.iter (fun (kwd, tok) -> Hashtbl.add keywords kwd tok) kwd


    (* Symbols Hashtable *)

    let sym =
        [|("+=",    (fun x -> ADDEQ(x)));
          ("-=",    (fun x -> SUBEQ(x)));
          ("*=",    (fun x -> MULTEQ(x)));
          ("/=",    (fun x -> DIVEQ(x)));
          ("%=",    (fun x -> MODEQ(x)));
          ("**=",   (fun x -> POWEQ(x)));
          ("//=",   (fun x -> FDIVEQ(x)));
          ("&=",    (fun x -> ANDEQ(x)));
          ("|=",    (fun x -> OREQ(x)));
          ("^=",    (fun x -> XOREQ(x)));
          ("<<=",   (fun x -> LSHEQ(x)));
          (">>=",   (fun x -> RSHEQ(x)));

          ("==",    (fun x -> EQUAL(x)));
          ("!=",    (fun x -> NOTEQ(x)));
          ("<>",    (fun x -> NOTEQ(x)));
          ("<=",    (fun x -> LEQ(x)));
          (">=",    (fun x -> GEQ(x)));
          ("<",     (fun x -> LT(x)));
          (">",     (fun x -> GT(x)));

          ("=",     (fun x -> EQ(x)));

          ("**",    (fun x -> POW(x)));
          ("//",    (fun x -> FDIV(x)));
          ("+",     (fun x -> ADD(x)));
          ("-",     (fun x -> SUB(x)));
          ("*",     (fun x -> MULT(x)));
          ("/",     (fun x -> DIV(x)));
          ("%",     (fun x -> MOD(x)));
          ("|",     (fun x -> BITOR(x)));
          ("&",     (fun x -> BITAND(x)));
          ("^",     (fun x -> BITXOR(x)));
          ("~",     (fun x -> BITNOT(x)));
          ("<<",    (fun x -> LSHIFT(x)));
          (">>",    (fun x -> RSHIFT(x)));

          ("(",     (fun x -> LPAREN(x)));
          (")",     (fun x -> RPAREN(x)));
          ("[",     (fun x -> LBRACK(x)));
          ("]",     (fun x -> RBRACK(x)));
          ("{",     (fun x -> LBRACE(x)));
          ("}",     (fun x -> RBRACE(x)));
          (":",     (fun x -> COLON(x)));
          (";",     (fun x -> SEMICOL(x)));
          (".",     (fun x -> DOT(x)));
          (",",     (fun x -> COMMA(x)));
          ("`",     (fun x -> BACKQUOTE(x)));
          ("@",     (fun x -> AT(x)));
          ("...",   (fun x -> ELLIPSIS(x)));
        |]
    let symbols = Hashtbl.create (Array.length sym)
    let _ = Array.iter (fun (sym, tok) -> Hashtbl.add symbols sym tok) sym
}

(* regexp *)

let e = ""

let newline = ('\n' | "\r\n")
let blank = [' ' '\t']
let comment = '#' [^ '\n' 'r']*

let digit = ['0'-'9']
let octdigit = ['0'-'7']
let hexdigit = ['0'-'9' 'a'-'f' 'A'-'Z']
let nonZeroDigit = ['1' - '9']

let integer = nonZeroDigit digit*
let octinteger = '0' octdigit+
let hexinteger = '0' ['x' 'X'] hexdigit+

let longintpostfix = ['l' 'L']
let intpart = digit+
let fraction = '.' digit+
let pointfloat = intpart? fraction | intpart '.'
let exponent = ['e' 'E'] ['+' '-']? digit+
let exponentfloat = (intpart | pointfloat) exponent
let floatnumber = pointfloat | exponentfloat
let imagnumber = (floatnumber | intpart) ['j' 'J']

let stringprefix = ('u' | 'U')? ('r' | 'R')?
let escapeseq = '\\' _

let identifier = ['a'-'z' 'A'-'Z' '_'] ['a'-'z' 'A'-'Z' '0'-'9' '_']*
let nonidchar = [^ 'a'-'z' 'A'-'Z' '0'-'9' '_']
let symb = "+=" | "-=" | "*=" | "/=" | "%=" | "**=" | "//=" | "&=" | "|=" | "^="
  | "<<=" | ">>=" | "==" | "!=" | "<>" | "<=" | ">=" | "<" | ">" | "=" | "**"
  | "//" | "+" | "-" | "*" | "/" | "%" | "|" | "&" | "^" | "~" | "<<" | ">>"
  | "(" | ")" | "[" | "]" | "{" | "}" | ":" | ";" | "." | "," | "`" | "@" | "..."

(* Rules *)

rule token state = parse
    | e {
        let curr_offset = state.curr_offset in
        let last_offset = Stack.top state.offset_stack in
            if curr_offset < last_offset then
                (ignore (Stack.pop state.offset_stack); DEDENT)
            else if curr_offset > last_offset then
                (Stack.push curr_offset state.offset_stack; INDENT)
            else
                _token state lexbuf}

and _token state = parse
  | ((blank* comment? newline)* blank* comment?) newline
      { let lines = count_lines (lexeme lexbuf) in
        let pos = lexbuf.lex_curr_p in
          lexbuf.lex_curr_p <-
            { pos with
                pos_bol = pos.pos_cnum;
                pos_lnum = pos.pos_lnum + lines };
        if state.nl_ignore <= 0 then begin
          state.curr_offset <- 0;
          offset state lexbuf;
          NEWLINE
        end else
          _token state lexbuf }
  | '\\' newline blank*
      { let pos = lexbuf.lex_curr_p in
          lexbuf.lex_curr_p <-
            { pos with
                pos_bol = pos.pos_cnum;
                pos_lnum = pos.pos_lnum + 1 };
          _token state lexbuf }

  | blank+
      { _token state lexbuf }

  | identifier as id {
      try (Hashtbl.find keywords id) (curr_pos lexbuf)
        with Not_found -> ID (id, (curr_pos lexbuf))  }
  | symb as s { (Hashtbl.find symbols s) (curr_pos lexbuf) }

  (* literals *)
  | integer as n longintpostfix
      { LONGINT (int_of_string n, curr_pos lexbuf) }
  | integer as n
      { INT (int_of_string n, curr_pos lexbuf) }
  | octinteger as n longintpostfix
      { LONGINT (int_of_string ("0o" ^ n), curr_pos lexbuf) }
  | octinteger as n
      { INT (int_of_string ("0o" ^ n), curr_pos lexbuf) }
  | hexinteger as n longintpostfix
      { LONGINT (int_of_string n, curr_pos lexbuf) }
  | hexinteger as n
      { INT (int_of_string n, curr_pos lexbuf) }
  | floatnumber as n
      { FLOAT (float_of_string n, curr_pos lexbuf) }
  | imagnumber as n
      { IMAG (n, curr_pos lexbuf) }
  | '0' longintpostfix
      { LONGINT (0, curr_pos lexbuf) }
  | '0'
      { INT (0, curr_pos lexbuf) }

  | stringprefix '\''
      { sq_shortstrlit state (curr_pos lexbuf) lexbuf }
  | stringprefix '"'
      { dq_shortstrlit state (curr_pos lexbuf) lexbuf }
  | stringprefix "'''"
      { sq_longstrlit state (curr_pos lexbuf) lexbuf }
  | stringprefix "\"\"\""
      { dq_longstrlit state (curr_pos lexbuf) lexbuf }

  (* eof *)
  | eof { ENDMARKER }

and offset state = parse
  | e { }
  | ' '  { state.curr_offset <- state.curr_offset + 1; offset state lexbuf }
  | '\t' { state.curr_offset <- state.curr_offset + 8; offset state lexbuf }

and sq_shortstrlit state pos = parse
  | (([^ '\\' '\r' '\n' '\''] | escapeseq)* as s) '\'' { STR (unescaped s, pos) }

and sq_longstrlit state pos = shortest
| (([^ '\\'] | escapeseq)* as s) "'''"
    { let lines = count_lines s in
      let curpos = lexbuf.lex_curr_p in
        lexbuf.lex_curr_p <- { curpos with pos_lnum = curpos.pos_lnum + lines };
        STR (unescaped s, pos) }

and dq_shortstrlit state pos = parse
  | (([^ '\\' '\r' '\n' '\"'] | escapeseq)* as s) '"' { STR (unescaped s, pos) }

and dq_longstrlit state pos = shortest
  | (([^ '\\'] | escapeseq)* as s) "\"\"\""
      { let lines = count_lines s in
        let curpos = lexbuf.lex_curr_p in
          lexbuf.lex_curr_p <- { curpos with pos_lnum = curpos.pos_lnum + lines };
          STR (unescaped s, pos) }
