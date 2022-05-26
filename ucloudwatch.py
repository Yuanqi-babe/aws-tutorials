import boto3

# 引用CloudWatch在特定区域的相关API
CW_client = boto3.client('cloudwatch', region_name='ap-southeast-1')

# 通过
# 1.构建监控时间，2. 可视化类型 3. 小组件在看板上的绝对位置 4. 小组件的长宽 5. 需要监控的指标类型 6. 单次监测刷新时间 7. 监测指标汇总方式 8. 小组件名称
# 9. 图例摆放位置 等信息，来自定义看板上小组件的内容。
dashboard_body = """
{
   "start": "-PT6H",
   "periodOverride": "inherit",
   "widgets": [
      {
         "type":"metric",
         "x":0,
         "y":0,
         "width":12,
         "height":6,
         "properties":{
            "metrics":[
               ["AWS/ElasticMapReduce","MRActiveNodes","JobFlowId","j-2SU5KB2AGD1JF",{"visible":false,"id":"m1"} ],
            [".","MRTotalNodes","JobFlowId","j-2SU5KB2AGD1JF",{"visible":false,"id":"m2"} ],
            [ { "expression": "100*(m1/m2)", "label": "EMRActiveNodesRatio", "id": "e3","visible":true } ]
            ],
            "period":300,
            "stat":"Average",
            "region":"ap-southeast-1",
            "title":"EMR Instance CoreNodes Running for j-2ACT3HJ3KZW0V",
            "liveData": false,
            "legend": {
                "position": "right"
              }
         }
      },
      {
         "type":"text",
         "x":15,
         "y":7,
         "width":3,
         "height":3,
         "properties":{
            "markdown":"Hello from BOTO5"
         }
      }
   ]
}
    """

# 最后，通过CloudWatch PutDashboard API更新控制看板的内容。
response = CW_client.put_dashboard(DashboardName='test',
                                   DashboardBody=dashboard_body)


# 如何添加自定义数学函数
# [ { "expression": "SUM(METRICS())", "label": "Sum of DiskReadbytes", "id": "e3" } ]
