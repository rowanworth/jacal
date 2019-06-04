[["python:package:icedefs"]]
#ifndef ASKAP_TYPEDVALUES_ICE
#define ASKAP_TYPEDVALUES_ICE

#include <CommonTypes.ice>

module askap
{

module interfaces
{
    /**
     * Enum to represent data types.
     **/
    enum TypedValueType {TypeNull, TypeFloat, TypeDouble, TypeInt, TypeLong,
                        TypeString, TypeBool, TypeFloatComplex, TypeDoubleComplex,
                        TypeFloatSeq, TypeDoubleSeq, TypeIntSeq, TypeLongSeq,
                        TypeStringSeq, TypeBoolSeq, TypeFloatComplexSeq,
                        TypeDoubleComplexSeq, TypeDirection, TypeDirectionSeq};
    
    /**
     * Base class for typed data types.
     **/
    class TypedValue { 
        TypedValueType type;
    };
   
    ///////////////////////////////////////////////
    // Primative data types
    ///////////////////////////////////////////////
 
    /**
     * Class for a float type.
     **/
    class TypedValueFloat extends TypedValue {
        float value;
    };
    
    /**
     * Class for a double precision float type.
     **/
    class TypedValueDouble extends TypedValue {
        double value;
    };
    
    /**
     * Class for an integer type.
     **/ 
    class TypedValueInt extends TypedValue {
        int value;
    };
    
    /**
     * Class for a long integer type.
     **/
    class TypedValueLong extends TypedValue {
        long value;
    };
    
    /**
     * Class for a string type.
     **/
    class TypedValueString extends TypedValue {
        string value;
    };
    
    /**
     * Class for a boolean type.
     **/
    class TypedValueBool extends TypedValue {
        bool value;
    };


    ///////////////////////////////////////////////
    // More advanced data types
    ///////////////////////////////////////////////
 
    /**
     * Class for a single precision floating point complex number.
     **/
    class TypedValueFloatComplex extends TypedValue {
        FloatComplex value;
    };

    /**
     * Class for a double precision floating point complex number.
     **/
    class TypedValueDoubleComplex extends TypedValue {
        DoubleComplex value;
    };

    /**
     * Class for astronomical direction
     **/
    class TypedValueDirection extends TypedValue {
        Direction value;
    };


    ///////////////////////////////////////////////
    // Sequences
    ///////////////////////////////////////////////
 
    /**
     * Class for a sequence of floats type.
     **/
    class TypedValueFloatSeq extends TypedValue {
        FloatSeq value;
    };

    /**
     * Class for a sequence of doubles type.
     **/
    class TypedValueDoubleSeq extends TypedValue {
        DoubleSeq value;
    };

    /**
     * Class for a sequence of integers type.
     **/
    class TypedValueIntSeq extends TypedValue {
        IntSeq value;
    };

    /**
     * Class for a sequence of long integers type.
     **/
    class TypedValueLongSeq extends TypedValue {
        LongSeq value;
    };

    /**
     * Class for a sequence of strings type.
     **/
    class TypedValueStringSeq extends TypedValue {
        StringSeq value;
    };

    /**
     * Class for a sequence of booleans type.
     **/
    class TypedValueBoolSeq extends TypedValue {
        BoolSeq value;
    };

    /**
     * Class for a sequence of single precision floating point complex number.
     **/
    class TypedValueFloatComplexSeq extends TypedValue {
        FloatComplexSeq value;
    };

    /**
     * Class for a sequence of double precision floating point complex number.
     **/
    class TypedValueDoubleComplexSeq extends TypedValue {
        DoubleComplexSeq value;
    };

    /**
     * Class for a sequence of direction typed
     **/
    class TypedValueDirectionSeq extends TypedValue {
        DirectionSeq value;
    };

    /**
     * Dictionary of typed data.
     **/
    dictionary <string,TypedValue> TypedValueMap;
    
    /**
     * Time-tagged dictionary of typed data.
     *
     * Timestamp is a Binary Atomic Time representing microseconds since
     * Modified Julian Date zero.
     */
    struct TimeTaggedTypedValueMap {
        long timestamp;
        TypedValueMap data;
    };

    module datapublisher
    {
        /**
         * Interface for a publisher of named typed values.
         **/
        interface ITypedValueMapPublisher {
            /**
             * Publish a new map of named typed values.
             **/
             void publish(TypedValueMap values);
        };

        /**
         * Interface for a publisher of time-tagged named typed values.
         **/
        interface ITimeTaggedTypedValueMapPublisher {
            /**
             * Publish a new map of named typed values.
             **/
             void publish(TimeTaggedTypedValueMap values);
        };
    };
};
};

#endif
