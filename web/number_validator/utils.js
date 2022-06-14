class NumberValidator{

    static inputs = undefined;

    constructor(input, allow_decimal=true, decimals = 2) {
        this.lastvalue = '';
        this.allow_decimal = allow_decimal;
        this.decimals = decimals;
        this.id = input.id;
        NumberValidator.inputs.set(this.id, this);
    }

    is_allowed(value){
        var ch = value.slice(value.length-1);
        var flag = undefined;
        if(this.allow_decimal && value.indexOf('.') == value.lastIndexOf('.'))
            flag = (value.indexOf('.')>0 && value.split('.')[1].length > this.decimals) ? false: "0123456789.".indexOf(ch)>=0;
        else
            flag = "0123456789".indexOf(ch)>=0;
        if(flag)
        {
            var test = value.slice(value.length-1) == '.' ? value+'0': value;
            var regex;
            var maxLength = 5;
            if(this.allow_decimal)
                regex = /^\d{1,9}(\.\d{1,9})?$/gm;
            else
                regex = /^\d{1,9}(\d{1,9})?$/gm;
            flag = regex.test(test)
        }
        return flag;
    }

    validate(value){
        if(value.length == 1 && value == '.')
            value = "0.0";
        else if(value.length >= 2 && value[0] == '0' && value[1] != '.')
            value = this.lastvalue;
        else if(value.length>0 && !this.is_allowed(value))
            value = this.lastvalue;
        this.lastvalue = value;
        return value;
    }

    static Validate(input, allow_decimal=true, decimals = 2){
        if(input.id != '' && input.id != undefined)
        {
            var validator=undefined;
            if(NumberValidator.inputs == undefined)
                NumberValidator.inputs = new Map();
            if (NumberValidator.inputs.has(input.id))
                validator = NumberValidator.inputs.get(input.id);
            else
                validator = new NumberValidator(input, allow_decimal, decimals);
            return validator.validate(input.value);
        }
        else {
            console.log("Input must have an id");
            return intput.value;
        }
    }

    static ValidateDecimal(input, decimals=2)
    {
        return NumberValidator.Validate(input, true, decimals);
    }

    static ValidateInteger(input)
    {
        return NumberValidator.Validate(input, false, 0);
    }

}