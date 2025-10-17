from colorama import Fore, Style, init
from modules.backup_manager import BackupManager

init(autoreset=True)

def show_banner():
    banner = f"""
{Fore.CYAN}                                                                                                                                         
                                                                                                                                         
                     ,;                           ,;  G:             L.                      ,;                                         .
                   f#i              i           f#i   E#,    :  t    EW:        ,ft        f#i                            t            ;W
  GEEEEEEEL      .E#t              LE         .E#t    E#t  .GE  Ej   E##;       t#E      .E#t                             Ej          f#E
  ,;;L#K;;.     i#W,              L#E        i#W,     E#t j#K;  E#,  E###t      t#E     i#W,          ,##############Wf.  E#,       .E#f 
     t#E       L#D.              G#W.       L#D.      E#GK#f    E#t  E#fE#f     t#E    L#D.            ........jW##Wt     E#t      iWW;  
     t#E     :K#Wfff;           D#K.      :K#Wfff;    E##D.     E#t  E#t D#G    t#E  :K#Wfff;                tW##Kt       E#t     L##Lffi
     t#E     i##WLLLLt         E#K.       i##WLLLLt   E##Wi     E#t  E#t  f#E.  t#E  i##WLLLLt             tW##E;         E#t    tLLG##L 
     t#E      .E#L           .E#E.         .E#L       E#jL#D:   E#t  E#t   t#K: t#E   .E#L               tW##E;           E#t      ,W#i  
     t#E        f#E:        .K#E             f#E:     E#t ,K#j  E#t  E#t    ;#W,t#E     f#E:          .fW##D,             E#t     j#E.   
     t#E         ,WW;      .K#D               ,WW;    E#t   jD  E#t  E#t     :K#D#E      ,WW;       .f###D,               E#t   .D#j     
     t#E          .D#;    .W#G                 .D#;   j#t       E#t  E#t      .E##E       .D#;    .f####Gfffffffffff;     E#t  ,WK,      
      fE            tt   :W##########Wt          tt    ,;       E#t  ..         G#E         tt   .fLLLLLLLLLLLLLLLLLi     E#t  EG.       
       :                 :,,,,,,,,,,,,,.                        ,;.              fE                                       ,;.  ,         
                                                                                  ,                                                      
{Style.RESET_ALL}
    """
    print(banner)

def main():
    show_banner()
    backup_manager = BackupManager()
    backup_manager.start()

if __name__ == "__main__":
    main()