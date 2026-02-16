insert into User(name,id,status,hours) values('Bob',1,'UNPAID',10)
insert into User(name,id,status,hours) values('Alice',0,'UNPAID',10)
insert into Topic(name,id) values('topic',0)
insert into ParticipationFee(amount,user,id) values(30,0,0)
insert into Exchange(source,planned_hours,id,effective_hours,status,destination) values(0,3,0,0,'PLANNED',None)
insert into TopicExchangeRelation(topic, exchange) values(0, 0)
update Exchange set effective_hours=3,status='DONE',destination=1 where id=0
