
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'OUT MOD RMEM JNZ RET JMP NOT MUL CALL NOP IN EQ ADD OR PUSH DB SET WMEM AND POP GT JZ HALT NUMBER LABEL REFERENCE COMMENT MATHOP LPAREN RPAREN CHAR STRING PLACEMENT REGISTERprogram : lineslines : line lineslines : lineline : PLACEMENT LABEL operation COMMENTline : LABEL operation COMMENTline : PLACEMENT operation COMMENTline : PLACEMENT LABEL COMMENTline : PLACEMENT LABEL operationline : operation COMMENTline : PLACEMENT COMMENTline : PLACEMENT LABEL line : LABEL COMMENTline : PLACEMENT operation line : LABEL operationline : PLACEMENTline : LABEL line : operationline : COMMENTline : emptyoperation : HALT\n            | SET args\n            | PUSH args\n            | POP args\n            | EQ args\n            | GT args\n            | JMP args\n            | JNZ args\n            | JZ args\n            | ADD args\n            | MUL args\n            | MOD args\n            | AND args\n            | OR args\n            | NOT args\n            | RMEM args\n            | WMEM args\n            | CALL args\n            | RET\n            | OUT args\n            | IN args\n            | NOP\n            | DB argsargs : arg argsargs : argarg : NUMBERarg : REGISTERarg : REFERENCEarg : CHARarg : STRINGarg : LPAREN expression RPARENexpression : NUMBER MATHOP NUMBERexpression : REFERENCE MATHOP NUMBERexpression : NUMBER MATHOP REFERENCEempty :'
    
_lr_action_items = {'PLACEMENT':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[4,4,-15,-16,-17,-18,-19,-20,-38,-41,-11,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'LABEL':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[5,5,33,-16,-17,-18,-19,-20,-38,-41,-11,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'COMMENT':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[7,7,35,37,38,-18,-19,-20,-38,-41,67,68,-10,69,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,74,-7,-6,-5,-43,-4,-50,]),'HALT':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[9,9,9,9,-17,-18,-19,-20,-38,-41,9,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'SET':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[10,10,10,10,-17,-18,-19,-20,-38,-41,10,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'PUSH':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[11,11,11,11,-17,-18,-19,-20,-38,-41,11,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'POP':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[12,12,12,12,-17,-18,-19,-20,-38,-41,12,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'EQ':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[13,13,13,13,-17,-18,-19,-20,-38,-41,13,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'GT':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[14,14,14,14,-17,-18,-19,-20,-38,-41,14,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'JMP':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[15,15,15,15,-17,-18,-19,-20,-38,-41,15,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'JNZ':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[16,16,16,16,-17,-18,-19,-20,-38,-41,16,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'JZ':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[17,17,17,17,-17,-18,-19,-20,-38,-41,17,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'ADD':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[18,18,18,18,-17,-18,-19,-20,-38,-41,18,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'MUL':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[19,19,19,19,-17,-18,-19,-20,-38,-41,19,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'MOD':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[20,20,20,20,-17,-18,-19,-20,-38,-41,20,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'AND':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[21,21,21,21,-17,-18,-19,-20,-38,-41,21,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'OR':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[22,22,22,22,-17,-18,-19,-20,-38,-41,22,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'NOT':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[23,23,23,23,-17,-18,-19,-20,-38,-41,23,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'RMEM':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[24,24,24,24,-17,-18,-19,-20,-38,-41,24,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'WMEM':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[25,25,25,25,-17,-18,-19,-20,-38,-41,25,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'CALL':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[26,26,26,26,-17,-18,-19,-20,-38,-41,26,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'RET':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[27,27,27,27,-17,-18,-19,-20,-38,-41,27,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'OUT':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[28,28,28,28,-17,-18,-19,-20,-38,-41,28,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'IN':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[29,29,29,29,-17,-18,-19,-20,-38,-41,29,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'NOP':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[30,30,30,30,-17,-18,-19,-20,-38,-41,30,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'DB':([0,3,4,5,6,7,8,9,27,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[31,31,31,31,-17,-18,-19,-20,-38,-41,31,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'$end':([0,1,2,3,4,5,6,7,8,9,27,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,74,75,],[-54,0,-1,-3,-15,-16,-17,-18,-19,-20,-38,-41,-2,-11,-13,-10,-14,-12,-9,-21,-44,-45,-46,-47,-48,-49,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-39,-40,-42,-8,-7,-6,-5,-43,-4,-50,]),'NUMBER':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,41,42,43,44,45,46,75,76,77,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,-45,-46,-47,-48,-49,72,-50,78,80,]),'REGISTER':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,41,42,43,44,45,75,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,-45,-46,-47,-48,-49,-50,]),'REFERENCE':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,41,42,43,44,45,46,75,76,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,-45,-46,-47,-48,-49,73,-50,79,]),'CHAR':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,41,42,43,44,45,75,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,-45,-46,-47,-48,-49,-50,]),'STRING':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,41,42,43,44,45,75,],[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,-45,-46,-47,-48,-49,-50,]),'LPAREN':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,41,42,43,44,45,75,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,-45,-46,-47,-48,-49,-50,]),'RPAREN':([71,78,79,80,],[75,-51,-53,-52,]),'MATHOP':([72,73,],[76,77,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'lines':([0,3,],[2,32,]),'line':([0,3,],[3,3,]),'operation':([0,3,4,5,33,],[6,6,34,36,66,]),'empty':([0,3,],[8,8,]),'args':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,],[39,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,70,]),'arg':([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,31,40,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'expression':([46,],[71,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> lines','program',1,'p_program','assembler.py',408),
  ('lines -> line lines','lines',2,'p_lines1','assembler.py',412),
  ('lines -> line','lines',1,'p_lines2','assembler.py',417),
  ('line -> PLACEMENT LABEL operation COMMENT','line',4,'p_line_ploc','assembler.py',422),
  ('line -> LABEL operation COMMENT','line',3,'p_line_loc','assembler.py',427),
  ('line -> PLACEMENT operation COMMENT','line',3,'p_line_poc','assembler.py',431),
  ('line -> PLACEMENT LABEL COMMENT','line',3,'p_line_plc','assembler.py',435),
  ('line -> PLACEMENT LABEL operation','line',3,'p_line_plo','assembler.py',439),
  ('line -> operation COMMENT','line',2,'p_line_oc','assembler.py',444),
  ('line -> PLACEMENT COMMENT','line',2,'p_line_pc','assembler.py',449),
  ('line -> PLACEMENT LABEL','line',2,'p_line_pl','assembler.py',453),
  ('line -> LABEL COMMENT','line',2,'p_line_lc','assembler.py',458),
  ('line -> PLACEMENT operation','line',2,'p_line_po','assembler.py',462),
  ('line -> LABEL operation','line',2,'p_line_lo','assembler.py',466),
  ('line -> PLACEMENT','line',1,'p_line_p','assembler.py',470),
  ('line -> LABEL','line',1,'p_line_l','assembler.py',474),
  ('line -> operation','line',1,'p_line_o','assembler.py',478),
  ('line -> COMMENT','line',1,'p_line_c','assembler.py',483),
  ('line -> empty','line',1,'p_line_e','assembler.py',487),
  ('operation -> HALT','operation',1,'p_operation','assembler.py',492),
  ('operation -> SET args','operation',2,'p_operation','assembler.py',493),
  ('operation -> PUSH args','operation',2,'p_operation','assembler.py',494),
  ('operation -> POP args','operation',2,'p_operation','assembler.py',495),
  ('operation -> EQ args','operation',2,'p_operation','assembler.py',496),
  ('operation -> GT args','operation',2,'p_operation','assembler.py',497),
  ('operation -> JMP args','operation',2,'p_operation','assembler.py',498),
  ('operation -> JNZ args','operation',2,'p_operation','assembler.py',499),
  ('operation -> JZ args','operation',2,'p_operation','assembler.py',500),
  ('operation -> ADD args','operation',2,'p_operation','assembler.py',501),
  ('operation -> MUL args','operation',2,'p_operation','assembler.py',502),
  ('operation -> MOD args','operation',2,'p_operation','assembler.py',503),
  ('operation -> AND args','operation',2,'p_operation','assembler.py',504),
  ('operation -> OR args','operation',2,'p_operation','assembler.py',505),
  ('operation -> NOT args','operation',2,'p_operation','assembler.py',506),
  ('operation -> RMEM args','operation',2,'p_operation','assembler.py',507),
  ('operation -> WMEM args','operation',2,'p_operation','assembler.py',508),
  ('operation -> CALL args','operation',2,'p_operation','assembler.py',509),
  ('operation -> RET','operation',1,'p_operation','assembler.py',510),
  ('operation -> OUT args','operation',2,'p_operation','assembler.py',511),
  ('operation -> IN args','operation',2,'p_operation','assembler.py',512),
  ('operation -> NOP','operation',1,'p_operation','assembler.py',513),
  ('operation -> DB args','operation',2,'p_operation','assembler.py',514),
  ('args -> arg args','args',2,'p_args1','assembler.py',521),
  ('args -> arg','args',1,'p_args2','assembler.py',525),
  ('arg -> NUMBER','arg',1,'p_arg_num','assembler.py',529),
  ('arg -> REGISTER','arg',1,'p_arg_reg','assembler.py',533),
  ('arg -> REFERENCE','arg',1,'p_arg_ref','assembler.py',537),
  ('arg -> CHAR','arg',1,'p_arg_char','assembler.py',541),
  ('arg -> STRING','arg',1,'p_arg_string','assembler.py',547),
  ('arg -> LPAREN expression RPAREN','arg',3,'p_arg_expression','assembler.py',556),
  ('expression -> NUMBER MATHOP NUMBER','expression',3,'p_expression_nmn','assembler.py',560),
  ('expression -> REFERENCE MATHOP NUMBER','expression',3,'p_expression_rmn','assembler.py',564),
  ('expression -> NUMBER MATHOP REFERENCE','expression',3,'p_expression_nmr','assembler.py',568),
  ('empty -> <empty>','empty',0,'p_empty','assembler.py',580),
]
