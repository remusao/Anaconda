{
    (* Header *)
    open Parser

    let kwd =
        [|("and",	    AND);
          ("del",	    DEL);
          ("from",	    FROM);
          ("not",	    NOT);
          ("while",	    WHILE);
          ("as",	    AS);
          ("elif",	    ELIF);
          ("global",	GLOBAL);
          ("or",	    OR);
          ("with",	    WITH);
          ("assert",	ASSERT);
          ("else",	    ELSE);
          ("if",	    IF);
          ("pass",	    PASS);
          ("yield",	    YIELD);
          ("break",	    BREAK);
          ("except",	EXCEPT);
          ("import",	IMPORT);
          ("print",	    PRINT);
          ("class",	    CLASS);
          ("exec",	    EXEC);
          ("in",	    IN);
          ("raise",	    RAISE);
          ("continue",  CONTINUE);
          ("finally",	FINALLY);
          ("is",	    IS);
          ("return",	RETURN);
          ("def",	    DEF);
          ("for",	    FOR);
          ("lambda",	LAMBDA);
          ("try",       TRY)|]
    let keywords = Hashtbl.create (Array.length kwd)
    let _ = Array.iter (fun (kwd, tok) -> Hashtbl.add keywords kwd tok) kwd


    let sym =
        [|("@",         AT);
          ("(",         LPAR);
          (")",         RPAR);
          (":",         COLON);
          ("=",         ASSIGN);
          (",",         COMA);
          ("*",         STAR);
          ("**",        POW);
          (";",         SEMICOLON);
          ("+=",        PLUSEQ);
          ("-=",        MINUSEQ);
          ("*=",        MULTEQ);
          ("/=",        DIVEQ);
          ("%=",        MODEQ);
          ("&=",        ANDEQ);
          ("|=",        OREQ);
          ("^=",        XOREQ);
          ("<<=",       LSEQ);
          (">>=",       RSEQ);
          ("**=",       POWEQ);
          ("//=",       DDIVEQ);
          (".",         DOT);
          ("...",       ELLIPSIS);
          (">",         GREATER);
          ("<",         LESSER);
          ("==",        EQUAL);
        |]
    let symbols = Hashtbl.create (Array.length sym)
    let _ = Array.iter (fun (sym, tok) -> Hashtbl.add symbols sym tok) sym
}


(* Body *)
