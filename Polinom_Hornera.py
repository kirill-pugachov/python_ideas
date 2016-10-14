# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 14:27:06 2016

@author: Кирилл
"""

Numbers = int(input('Укажите длинну полинома – кол-во членов для расчета:'))
Point = int(input('Укажите значение точки для вычисления полинома:'))

Ratio=[]

for I in range(0, Numbers):
    Ratio.append(int(input('Введите значение коэф-та' + str(I) + 'члена полинома: ')))
Result=Ratio[0]+Ratio[1]*Point
Sum=Point
for I in range(2, Numbers):
    Sum=Sum*Point
    Result=Ratio[I]*Sum
  
print ('Значение полинома Горнера в точке' + str(Point) + 'равно:', Result)