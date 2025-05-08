# Documentation

## Guidelines in a Twincatproject

Only tags between the fb name and the first var block are parsed
Multiline is possible
Usage can be rendered to show as code

Only in, out, and in/out variable blocks are rendered. internal blocks are not rendered.

```
    FUNCTION_BLOCK FB_AdjustAssertFailureMessageToMax253CharLength
    //
    //@details This FunctionBlock does this and that.
    //@usage use the functionblock like that. here is an example: FB_AdjustAssert.....
    //@returns makes no sense at a fb. can be used at a method
    //
    //@tag1 there can be custom tags written. they will be rendered after the standard tags above
    //@tag3 another tag
    //
    //
    VAR_INPUT
        TestInstancePath : T_MaxString; // everything that goes behind here is parsed as a detail of the variable
        TestMessage : T_MaxString; // another detail
    END_VAR
    VAR_OUTPUT
        TestInstancePathProcessed : T_MaxString;
        TestMessageProcessed : T_MaxString;
    END_VAR
    VAR_TEMP
        TestInstancePathTemporary : T_MaxString;
    END_VAR
    VAR CONSTANT
        MESSAGE_FORMATTED_STRING_MAX_NUMBER_OF_CHARACTERS : INT := 253; // This is actually 254, but if StrArg-argument is used (which it is in TcUnit) it is 253.
        TEST_NAME_TOO_LONG : STRING := '...TestName too long';
        TEST_MESSAGE_TOO_LONG : STRING := '...TestMsg too long';
    END_VAR
```