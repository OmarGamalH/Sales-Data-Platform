import Utilities.Utilities as u
import pydeequ as pd
import pydeequ.analyzers as analyzers
import pyspark.sql.functions as f
import pyspark.sql.types as types
spark = u.spark


def AddressDP(RawDataFrame , status):

    AddressAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)

    AddressAnalyzerResult = AddressAnalyzer\
    .addAnalyzer(analyzers.Completeness("AddressLine1"))\
    .addAnalyzer(analyzers.Minimum("StateProvinceID"))\
    .addAnalyzer(analyzers.Maximum("StateProvinceID"))\
    .addAnalyzer(analyzers.Size())\
    .addAnalyzer(analyzers.CountDistinct(["AddressLine1", "AddressLine2" , "City","StateProvinceID" , "PostalCode"]))\
    .addAnalyzer(analyzers.MinLength("AddressLine1"))\
    .addAnalyzer(analyzers.MaxLength("AddressLine1"))\
    .addAnalyzer(analyzers.MinLength("City"))\
    .addAnalyzer(analyzers.MaxLength("City"))\
    .run()

    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , AddressAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "Address" , status)

    return Final_DP_DF



def CreditCardDP(RawDataFrame , status):
    CreditCardAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)
    

    CreditCardAnalyzerResult = CreditCardAnalyzer\
                                .addAnalyzer(analyzers.MinLength("CardNumber"))\
                                .addAnalyzer(analyzers.MaxLength("CardNumber"))\
                                .addAnalyzer(analyzers.Minimum("ExpMonth"))\
                                .addAnalyzer(analyzers.Maximum("ExpMonth"))\
                                .addAnalyzer(analyzers.CountDistinct("CardNumber"))\
                                .addAnalyzer(analyzers.Size())\
                                .run()
    

    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , CreditCardAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "CreditCard" , status)

    return Final_DP_DF



def ShipMethodDP(RawDataFrame , status):
    
    RawDataFrame = RawDataFrame.withColumn("ShipBase" , f.col("ShipBase").cast(types.DecimalType(10 , 4)))\
                                .withColumn("ShipRate" , f.col("ShipRate").cast(types.DecimalType(10 , 4)))


    ShipMethodAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)

    ShipMethodAnalyzerResult = ShipMethodAnalyzer\
                                    .addAnalyzer(analyzers.CountDistinct("Name"))\
                                    .addAnalyzer(analyzers.Minimum("ShipBase"))\
                                    .addAnalyzer(analyzers.Maximum("ShipBase"))\
                                    .addAnalyzer(analyzers.Minimum("ShipRate"))\
                                    .addAnalyzer(analyzers.Maximum("ShipRate"))\
                                    .addAnalyzer(analyzers.Size())\
                                    .run()
        

    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , ShipMethodAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "ShipMethod" , status)

    return Final_DP_DF




def TerritoryDP(RawDataFrame , status):
    RawDataFrame = RawDataFrame.withColumn("SalesYTD" , f.col("SalesYTD").cast(types.DecimalType(20 , 4)))\
                               .withColumn("SalesLastYear" , f.col("SalesLastYear").cast(types.DecimalType(20 , 4)))\
                               .withColumn("CostYTD" , f.col("CostYTD").cast(types.DecimalType(20 , 4)))\
                               .withColumn("CostLastYear" , f.col("CostLastYear").cast(types.DecimalType(20 , 4)))

    TerritoryAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)
    
    TerritoryAnalyzerResult = TerritoryAnalyzer\
                                    .addAnalyzer(analyzers.CountDistinct("Name"))\
                                    .addAnalyzer(analyzers.Size())\
                                    .addAnalyzer(analyzers.Completeness("Name"))\
                                    .addAnalyzer(analyzers.Completeness("CountryRegionCode"))\
                                    .addAnalyzer(analyzers.Completeness("Group"))\
                                    .addAnalyzer(analyzers.Minimum("SalesYTD"))\
                                    .addAnalyzer(analyzers.Maximum("SalesYTD"))\
                                    .addAnalyzer(analyzers.Minimum("SalesLastYear"))\
                                    .addAnalyzer(analyzers.Maximum("SalesLastYear"))\
                                    .addAnalyzer(analyzers.Minimum("CostYTD"))\
                                    .addAnalyzer(analyzers.Maximum("CostYTD"))\
                                    .addAnalyzer(analyzers.Minimum("CostLastYear"))\
                                    .addAnalyzer(analyzers.Maximum("CostLastYear"))\
                                    .run()
        

    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , TerritoryAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "Territory" , status)

    return Final_DP_DF



def StoreDP(RawDataFrame , status):
        StoreAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)
                         
        StoreAnalyzerResult = StoreAnalyzer\
                            .addAnalyzer(analyzers.Size())\
                            .addAnalyzer(analyzers.CountDistinct("Name"))\
                            .addAnalyzer(analyzers.Uniqueness(["Name"]))\
                            .run()
                
        DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , StoreAnalyzerResult)

        Final_DP_DF = u.DataQualityProcessing(DP_DF , "Store" , status)

        return Final_DP_DF



def PersonDP(RawDataFrame , status):
    PersonAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)
                    
    PersonAnalyzerResult = PersonAnalyzer\
                        .addAnalyzer(analyzers.Completeness("PersonType"))\
                        .addAnalyzer(analyzers.Completeness("Title"))\
                        .addAnalyzer(analyzers.MinLength("FirstName"))\
                        .addAnalyzer(analyzers.MaxLength("FirstName"))\
                        .addAnalyzer(analyzers.MinLength("MiddleName"))\
                        .addAnalyzer(analyzers.MaxLength("MiddleName"))\
                        .addAnalyzer(analyzers.MinLength("LastName"))\
                        .addAnalyzer(analyzers.MaxLength("LastName"))\
                        .addAnalyzer(analyzers.Size())\
                        .run()
        
    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , PersonAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "Person" , status)

    return Final_DP_DF


def CurrencyRateDP(RawDataFrame , status):
    RawDataFrame = RawDataFrame.withColumn("AverageRate" , f.col("AverageRate").cast(types.DecimalType(10 , 4)))\
                               .withColumn("EndOfDayRate" , f.col("EndOfDayRate").cast(types.DecimalType(10 , 4)))

    CurrencyRateAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)
                
    CurrencyRateAnalyzerResult = CurrencyRateAnalyzer\
                        .addAnalyzer(analyzers.MinLength("FromCurrencyCode"))\
                        .addAnalyzer(analyzers.MaxLength("FromCurrencyCode"))\
                        .addAnalyzer(analyzers.MinLength("ToCurrencyCode"))\
                        .addAnalyzer(analyzers.MaxLength("ToCurrencyCode"))\
                        .addAnalyzer(analyzers.Minimum("AverageRate"))\
                        .addAnalyzer(analyzers.Maximum('AverageRate'))\
                        .addAnalyzer(analyzers.Maximum("EndOfDayRate"))\
                        .addAnalyzer(analyzers.Minimum("EndOfDayRate"))\
                        .addAnalyzer(analyzers.Size())\
                        .run()
        
    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , CurrencyRateAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "CurrencyRate" , status)

    return Final_DP_DF
    



def SalesOrderHeaderDP(RawDataFrame , status):

    RawDataFrame = RawDataFrame.withColumn("SubTotal" , f.col("SubTotal").cast(types.DecimalType(10 , 4)))\
                                .withColumn("TaxAmt" , f.col("TaxAmt").cast(types.DecimalType(10 , 4)))\
                                .withColumn("Freight" , f.col("Freight").cast(types.DecimalType(10 , 4)))\
                                .withColumn("TotalDue" , f.col("TotalDue").cast(types.DecimalType(10 , 4)))
    SalesOrderHeaderAnalyzer = analyzers.AnalysisRunner(spark).onData(RawDataFrame)
                
    SalesOrderHeaderAnalyzerResult = SalesOrderHeaderAnalyzer\
                        .addAnalyzer(analyzers.Size())\
                        .addAnalyzer(analyzers.Minimum("SubTotal"))\
                        .addAnalyzer(analyzers.Maximum("SubTotal"))\
                        .addAnalyzer(analyzers.Minimum("TaxAmt"))\
                        .addAnalyzer(analyzers.Maximum("TaxAmt"))\
                        .addAnalyzer(analyzers.Minimum("Freight"))\
                        .addAnalyzer(analyzers.Maximum("Freight"))\
                        .addAnalyzer(analyzers.Minimum("TotalDue"))\
                        .addAnalyzer(analyzers.Maximum("TotalDue"))\
                        .run()
        
    DP_DF = analyzers.AnalyzerContext.successMetricsAsDataFrame(spark , SalesOrderHeaderAnalyzerResult)

    Final_DP_DF = u.DataQualityProcessing(DP_DF , "SalesOrderHeader" , status)

    return Final_DP_DF
