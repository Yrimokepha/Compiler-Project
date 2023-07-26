import basic2

while True:
    text= input( 'basic >' )
    result,error = basic2.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)
    