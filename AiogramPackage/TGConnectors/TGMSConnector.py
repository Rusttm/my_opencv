from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
import os
import logging

class TGMSConnector(MSGSControllerAsync):
    logger_name = f"{os.path.basename(__file__)}"

    def __init__(self):
        super().__init__()

    async def get_account_rep_str_async(self):
        res_str = str()
        try:
            account_res_dict = await self.save_daily_accounts_gs_async()
            gs_href = account_res_dict.get("info").get("gs_href")
            total = account_res_dict.get("info").get("total", 0)
            ws_id = account_res_dict.get("info").get("gs_ws_id", 0)
        except Exception as e:
            res_str = f"Отчет по остаткам на счетах не сформирован, Ошибка: \n {e}"
            self.logger.warning(res_str)
            logging.warning(res_str)
        else:
            res_str = f"<a href='{gs_href + '/edit#gid=' + str(ws_id)}'>💰Денег на <b>счетах:</b> {int(total)}руб.</a>\n"
        return res_str
    async def get_debt_rep_str_async(self):
        res_str = str()
        try:
            res_dict = await self.save_daily_debt_gs_async()
            gs_href = res_dict.get("info").get("gs_href")
            ws_id = res_dict.get("info").get("gs_ws_id", 0)
            total = res_dict.get("info").get("total")
        except Exception as e:
            res_str = f"Отчет по задолженностям не сформирован, Ошибка: \n {e}"
            self.logger.warning(res_str)
            logging.warning(res_str)
        else:
            res_str = f"<a href='{gs_href + '/edit#gid=' + str(ws_id)}'>🚬<b>Задолженность</b> клиентов на сегодня: {int(total)}руб.</a>\n"
        return res_str
    async def get_profit_rep_str_async(self):
        res_str = str()
        try:
            res_dict = await self.save_profit_gs_daily_async()
            gs_href = res_dict.get("info").get("gs_href")
            ws_id = res_dict.get("info").get("gs_ws_id", 0)
            total = res_dict.get("info").get("total")
        except Exception as e:
            res_str = f"Отчет по прибыли не сформирован, Ошибка: \n {e}"
            self.logger.warning(res_str)
            logging.warning(res_str)
        else:
            res_str = f"<a href='{gs_href + '/edit#gid=' + str(ws_id)}'>💸<b>Прибыль</b> по месяцу: {int(total)}руб.</a>\n"
        return res_str
    async def get_bal_rep_str_async(self):
        res_str = str()
        try:
            res_dict = await self.save_balance_gs_async()
            gs_href = res_dict.get("info").get("gs_href")
            ws_id = res_dict.get("info").get("gs_ws_id", 0)
            total = res_dict.get("info").get("total")
        except Exception as e:
            res_str = f"Отчет по балансам не сформирован, Ошибка: \n {e}"
            self.logger.warning(res_str)
            logging.warning(res_str)
        else:
            res_str = f"<a href='{gs_href + '/edit#gid=' + str(ws_id)}'>⚖️<b>Баланс</b> на сегодня: {int(total)}руб.</a>\n"
        return res_str
    async def get_margins_rep_str_async(self):
        res_str = str()
        try:

            res_dict = await self.save_daily_margins_gs_async()
            # res_dict = await controller.save_custom_margins_gs_async(from_date="2023-01-9", to_date="2023-01-9")
            gs_href = res_dict.get("info").get("gs_href")
            ws_id = res_dict.get("info").get("gs_ws_id", 0)
            margin = res_dict.get("info").get("margin", 30)
            total = res_dict.get("info").get("total")

            if total == 0:
                res_str = f"<a href='{gs_href + '/edit#gid=' + str(ws_id)}'>🛠️<b>Отгрузок</b> меньше {margin}% нет 🤷🏼‍</a>"
            else:
                try:
                    res_str = f"<a href='{gs_href + '/edit#gid=' + str(ws_id)}'>🛠️{int(total)}шт. <b>Отгрузок</b> с прибылью меньше {margin}%: </a>\n"
                    margins_list = res_dict.get("data")
                    for client_dict in margins_list:
                        res_str += f"{client_dict.get('name')}: {client_dict.get('sale')}руб ({client_dict.get('profitability')}%) \n"
                except Exception as e:
                    self.logger.warning(f"Cant load margins report, Error:\n {e}")
                    logging.warning(res_str)
        except Exception as e:
            res_str = f"Отчет низкой прибыли не сформирован, Ошибка: \n {e}"
            self.logger.warning(res_str)
            logging.warning(res_str)
        return res_str
    async def get_summary_rep_str_async(self):
        res_str = str()
        try:
            bal_str = await self.get_bal_rep_str_async()
            profit = await self.get_profit_rep_str_async()
            account_str = await self.get_account_rep_str_async()
            margin_str = await self.get_margins_rep_str_async()
        except Exception as e:
            res_str = f"Отчет по остаткам на счетах не сформирован, Ошибка \n {e}"
            self.logger.warning(f"Cant load margins report, Error:\n {e}")
            logging.warning(res_str)
        else:
            res_str = str(bal_str + profit + account_str + margin_str)
        return res_str
