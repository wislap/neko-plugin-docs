HTTP API 端点
=============

Plugin Server 提供以下 HTTP API 端点：

插件管理
--------

.. list-table::
   :widths: 15 30 55
   :header-rows: 1

   * - 方法
     - 端点
     - 说明
   * - GET
     - ``/plugins``
     - 列出所有已注册插件
   * - GET
     - ``/plugins/{plugin_id}``
     - 获取插件详情
   * - POST
     - ``/plugin/trigger``
     - 触发插件入口点

Run 管理
--------

.. list-table::
   :widths: 15 30 55
   :header-rows: 1

   * - 方法
     - 端点
     - 说明
   * - POST
     - ``/runs``
     - 创建 Run
   * - GET
     - ``/runs/{run_id}``
     - 查询 Run 状态
   * - POST
     - ``/runs/{run_id}/cancel``
     - 取消 Run
   * - GET
     - ``/runs/{run_id}/export``
     - 获取 Run 的 Export 列表
   * - WS
     - ``/runs/{run_id}/ws``
     - WebSocket 实时推送
