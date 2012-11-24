let main () =
    if Array.length Sys.argv >= 2 then
    begin
        let lexbuf = Lexing.from_channel (open_in (Sys.argv.(1))) in
        let state = Lexer_state.create () in
        let ast = Parser.file_input (Lexer.token state) lexbuf in
        ()
    end;
    exit 0

let _ = main ()
