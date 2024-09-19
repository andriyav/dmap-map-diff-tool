def query_content_type(mls_num):
    return f''' select ctm.content_sub_type
from download_mls dm
left join mls m ON m.id = dm.mls_id
left join download_config dc on dc.id  = dm.download_config_id
left join mls_resource mr on mr.mls_id = dm.mls_id
left join process_map pm on pm.id = mr.process_map_id
left join content_type_map ctm on ctm.id = mr.content_type_map_id
left join download_protocol dp on dp.id = dc.download_protocol_id
where m.id = {mls_num}
and m.is_parent_mls = true
and pm.properties is not null'''


def query_map(mls_num, content_type):
    return f''' select pm.properties
        from download_mls dm 
        left join mls m ON m.id = dm.mls_id 
        left join download_config dc on dc.id  = dm.download_config_id 
        left join mls_resource mr on mr.mls_id = dm.mls_id  
        left join process_map pm on pm.id = mr.process_map_id 
        left join content_type_map ctm on ctm.id = mr.content_type_map_id 
        left join download_protocol dp on dp.id = dc.download_protocol_id 
            where ctm.content_sub_type = '{content_type}'
        and m.id = {mls_num}
        and m.is_parent_mls = true
        and pm.properties is not null'''