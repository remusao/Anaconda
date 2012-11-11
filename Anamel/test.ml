
type token =
       AND
     | DEL
     | FROM
     | NOT
     | WHILE
     | AS
     | ELIF
     | GLOBAL
     | OR
     | WITH
     | ASSERT
     | ELSE
     | IF
     | PASS
     | YIELD
     | BREAK
     | EXCEPT
     | IMPORT
     | PRINT
     | CLASS
     | EXEC
     | IN
     | RAISE
     | CONTINUE
     | FINALLY
     | IS
     | RETURN
     | DEF
     | FOR
     | LAMBDA
     | TRY
     | OTHER

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
