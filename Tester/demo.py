import util
times = 1
print('你好，我是聊天机器人-小象宝宝。\n有人说我有10岁人类的智商，你想试试吗？\n我可以回答你3个问题，来吧。')
while True:
    me = input('第{}个问题：'.format(times))
    print('小象宝宝：' + util.talk(me))
    if me == '再见' or times >= 3:
        print('小象宝宝：我要走了，祝你学得快乐，再见！')
        break
    times += 1